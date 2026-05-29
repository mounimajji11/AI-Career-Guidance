// ================= REGISTER USER DATA (PERSISTENT) =================

function registerUser(event) {

    event?.preventDefault();

    const name =
        document.querySelector('#registerPage input[type="text"]').value;

    const email =
        document.querySelector('#registerPage input[type="email"]').value;

    const password =
        document.querySelector('#registerPage input[type="password"]').value;

    if (!name || !email || !password) {

        alert("Please fill all registration details");

        return;
    }

    if (password.length < 8) {

        alert("Password must be at least 8 characters");

        return;
    }

    localStorage.setItem("email", email);
    localStorage.setItem("password", password);

    alert("Registration Successful");

    document.getElementById("registerPage")
        .classList.add("hidden");

    document.getElementById("loginPage")
        .classList.remove("hidden");
}


// ================= LOGIN CHECK =================

function openDashboard(event) {

    event?.preventDefault();

    const email =
        document.querySelector('#loginPage input[type="email"]').value;

    const password =
        document.querySelector('#loginPage input[type="password"]').value;

    const savedEmail = localStorage.getItem("email");
    const savedPassword = localStorage.getItem("password");

    if (!email || !password) {

        alert("Please enter email and password");

        return;
    }

    if (!savedEmail || !savedPassword) {

        alert("Please register first");

        return;
    }

    if (email !== savedEmail) {

        alert("Invalid Email");

        return;
    }

    if (password !== savedPassword) {

        alert("Incorrect Password");

        return;
    }

    document.getElementById("loginPage")
        .classList.add("hidden");

    document.getElementById("dashboardPage")
        .classList.remove("hidden");
}


// ================= NAVIGATION =================

function openLogin() {

    document.getElementById("heroPage")
        .classList.add("hidden");

    document.getElementById("registerPage")
        .classList.add("hidden");

    document.getElementById("loginPage")
        .classList.remove("hidden");
}

function openRegister() {

    document.getElementById("loginPage")
        .classList.add("hidden");

    document.getElementById("registerPage")
        .classList.remove("hidden");
}


// ================= PREDICTION =================

async function showResultPage() {

    const attendance =
        Number(document.getElementById("attendance").value);

    const coding =
        Number(document.getElementById("coding").value);

    const aptitude =
        Number(document.getElementById("aptitude").value);

    const communication =
        Number(document.getElementById("communication").value);

    const projects =
        Number(document.getElementById("projects").value);

    const certifications =
        Number(document.getElementById("certifications").value);

    if (
        !attendance &&
        !coding &&
        !aptitude &&
        !communication &&
        !projects &&
        !certifications
    ) {

        alert("Please fill all student details");

        return;
    }

    try {

        const response = await fetch('/predict', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({

                attendance,
                coding,
                aptitude,
                communication,
                projects,
                certifications

            })
        });

        const data = await response.json();

        console.log("BACKEND RESPONSE:", data);

        document.getElementById("dashboardPage")
            .classList.add("hidden");

        document.getElementById("resultPage")
            .classList.remove("hidden");

        // ================= SCORE =================

        let score = Number(data.linear_score);

        if (isNaN(score) || score <= 0) {

            score =
                (
                    attendance +
                    coding +
                    aptitude +
                    communication +
                    (projects * 10) +
                    (certifications * 10)
                ) / 5;
        }

        document.getElementById("score")
            .innerText = score.toFixed(2);

        // ================= CAREER =================

        let career = data.career;

        if (!career || career === "Software Developer") {

            if (
                coding >= 85 &&
                aptitude >= 80
            ) {

                career = "AI Engineer";
            }

            else if (
                communication >= 85 &&
                aptitude >= 75
            ) {

                career = "Business Analyst";
            }

            else if (
                projects >= 4 &&
                coding >= 70
            ) {

                career = "Full Stack Developer";
            }

            else if (coding >= 60) {

                career = "Software Developer";
            }

            else {

                career = "Technical Support";
            }
        }

        document.getElementById("career")
            .innerText = career;

        // ================= SKILL =================

        document.getElementById("skill")
            .innerText =
            data.performance || "Intermediate";

        // ================= ELIGIBILITY =================

        let placementStatus;

        if (
            attendance >= 70 &&
            coding >= 60 &&
            aptitude >= 60
        ) {

            placementStatus = "Eligible";
        }

        else {

            placementStatus = "Not Eligible";
        }

        document.getElementById("placement")
            .innerText = placementStatus;

    }

    catch (error) {

        console.log(error);

        alert("Backend connection failed");
    }
}


// ================= BACK =================

function backDashboard() {

    document.getElementById("resultPage")
        .classList.add("hidden");

    document.getElementById("dashboardPage")
        .classList.remove("hidden");
}