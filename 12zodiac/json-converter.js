const fs = require('fs');
const path = require('path');

// Read the input file
const inputFile = 'zodiac-predictions.json';
const outputFile = '/Users/jeff/Documents/BitBucket/xianghuo/src/data/2025.12z.data.json';

// Read the JSON file
const rawData = fs.readFileSync(inputFile, 'utf8');
const inputData = JSON.parse(rawData);

// Create a new object to store the reverted data
const revertedData = [{
    id: "01JFAHZM27Z6C0FFP4RJ59KYDS",
    title: "Pokkoa 蛇年12生肖开运图",
    desc: "",
    items: []
}];

function readfile(filename) {
    try {
        console.log("reading: ",filename, "")
        // Construct the full path to the file
        const filePath = path.join(__dirname, filename);
        // Read the file synchronously
        return fs.readFileSync(filePath, 'utf8');
    } catch (error) {
        console.error(`Error reading file ${filename}:`, error);
        return "默认文本内容";
    }
}

// Counter for dynamic ID generation
let itemId = 1;

// Process each zodiac sign in the input data
Object.keys(inputData).forEach(key => {
    // Skip metadata
    if (key === 'metadata') return;

    const zodiacData = inputData[key];
    const item = {
        id: itemId,
        title: key,
        punchline: zodiacData.运势 && zodiacData.运势[0] ? zodiacData.运势[0] : "默认标语",
        caption: zodiacData.运势 && zodiacData.运势[1] ? zodiacData.运势[1] : "默认描述",
        img: "2025-12z-"+itemId,
        text: readfile(`./out/${zodiacData.chineseZodiac}_shorten_2.txt`),
        long: readfile(`./out/${zodiacData.chineseZodiac}_prompt2_2.txt`),
        outlier: zodiacData.特殊情况,
        fortune: zodiacData.运势,
        critical: zodiacData.需要注意的领域,
        actions: [] // You can modify this if needed,
    };
    itemId++
    //console.log(item)
    revertedData[0].items.push(item);
});

// Write the reverted data to a new JSON file
fs.writeFileSync(outputFile, JSON.stringify(revertedData, null, 2), 'utf8');

console.log('Reversion complete. Output saved to', outputFile);