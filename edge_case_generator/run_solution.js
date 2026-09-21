const solution=require("../solution.js");
// const testCase=[4,5,6,7,6,5];
// console.log(solution(testCase))
const testCase=JSON.parse(process.argv[2])  //turn the text into array
console.log(JSON.stringify(solution(testCase)))