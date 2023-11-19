document.getElementById("btn").onclick = function(){
    let uid = document.getElementById("user").value
    let pwd = document.getElementById("pwd").value
    if(uid !== "001"){
        alert("正确")
    }else{
        alert("错误")
    }
}