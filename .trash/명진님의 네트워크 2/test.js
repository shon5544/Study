const request = async (num) => {
    await fetch("http://52.78.159.231:8080/").then((res) => {
        console.log(`${res.status}: ${num}번 응답 완료`)
    })
}

const makeRequests = async () => {
    for (let i = 0; i < 100; i++) {
        request(i);
    }
}

makeRequests();