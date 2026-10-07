// MOST FREQUENT CONSECUTIVE SERIES --acsending  and descending
function solution(a){
    let longest_sequence=[];
    let current_sequence=[];
    let direction=0  //direction resets to zero for brand new sequence

    for(let i=0; i<a.length-1;i++){
        let diff=a[i]-a[i+1];
        if(diff!==-1 && diff!==1){
            current_sequence=[]
            direction=0;
        }
        else if(direction===0){
            current_sequence.push(a[i]);
            current_sequence.push(a[i+1]);
            direction=diff;
        }
        else if(direction===diff){
            current_sequence.push(a[i+1]);
        }
        else{  //dircetion!==diff --direction has changed
            current_sequence=[a[i]]
            direction=0;
        }
        

        if (current_sequence.length > longest_sequence.length) {
                longest_sequence = [...current_sequence];
        }
    }

    return longest_sequence;
}

module.exports=solution;  //make the function importable

//manual testing --but what if I missed a case that would catch a bug in my code
// console.log(solution([1,2,3,2]));
// console.log(solution([4, 5, 6, 7, 2, 3]));
// console.log(solution([1,2,3,4]));
// console.log(solution([1,5,10,4]));
// console.log(solution([3,2,1,4]));
// console.log(solution([4,5,6,7,6,5]));
// console.log(solution([4,5,6,7,6,5,4,3,2,1]));
// console.log(solution([1,2,3,10,11,12,13]));
// console.log(solution([1, 2, 3, 2, 1, 0, -1]));