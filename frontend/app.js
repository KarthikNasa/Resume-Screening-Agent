const jobDescription =
    document.getElementById(
        "jobDescription"
    );


const resumeFiles =
    document.getElementById(
        "resumeFiles"
    );


const dropZone =
    document.getElementById(
        "dropZone"
    );


const fileList =
    document.getElementById(
        "fileList"
    );


const analyzeButton =
    document.getElementById(
        "analyzeButton"
    );


const loading =
    document.getElementById(
        "loading"
    );


const errorMessage =
    document.getElementById(
        "errorMessage"
    );


const resultsSection =
    document.getElementById(
        "resultsSection"
    );


let selectedFiles = [];


/* =========================================
   FILE SELECTION
========================================= */


resumeFiles.addEventListener(
    "change",
    function () {

        addFiles(
            Array.from(
                resumeFiles.files
            )
        );

    }
);


/* =========================================
   DRAG AND DROP
========================================= */


dropZone.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        dropZone.classList.add(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "dragleave",
    function () {

        dropZone.classList.remove(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        dropZone.classList.remove(
            "dragover"
        );

        addFiles(
            Array.from(
                event.dataTransfer.files
            )
        );

    }
);


/* =========================================
   ADD FILES
========================================= */


function addFiles(files) {

    for (const file of files) {

        const extension =
            file.name
                .split(".")
                .pop()
                .toLowerCase();


        if (
            extension !== "pdf" &&
            extension !== "docx"
        ) {

            showError(
                `${file.name}: `
                + "Only PDF and DOCX files "
                + "are supported."
            );

            continue;
        }


        const alreadyExists =
            selectedFiles.some(
                existing =>
                    existing.name === file.name
                    &&
                    existing.size === file.size
            );


        if (!alreadyExists) {

            selectedFiles.push(file);

        }

    }


    renderFileList();

}


/* =========================================
   RENDER FILE LIST
========================================= */


function renderFileList() {

    fileList.innerHTML = "";


    if (
        selectedFiles.length === 0
    ) {

        return;

    }


    selectedFiles.forEach(
        (file, index) => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "file-item";


            const size =
                formatFileSize(
                    file.size
                );


            item.innerHTML = `

                <div>
                    <strong>
                        ${escapeHtml(
                            file.name
                        )}
                    </strong>

                    <div
                        class="file-size"
                    >
                        ${size}
                    </div>
                </div>

                <button
                    type="button"
                    onclick="removeFile(${index})"
                >
                    Remove
                </button>

            `;


            fileList.appendChild(
                item
            );

        }
    );

}


/* =========================================
   REMOVE FILE
========================================= */


function removeFile(index) {

    selectedFiles.splice(
        index,
        1
    );

    renderFileList();

}


/* =========================================
   ANALYZE
========================================= */


analyzeButton.addEventListener(
    "click",
    analyzeResumes
);


async function analyzeResumes() {

    clearError();


    if (
        !jobDescription.value.trim()
    ) {

        showError(
            "Please enter a job description."
        );

        return;

    }


    if (
        selectedFiles.length === 0
    ) {

        showError(
            "Please upload at least one resume."
        );

        return;

    }


    const formData =
        new FormData();


    formData.append(
        "job_description",
        jobDescription.value
    );


    selectedFiles.forEach(
        file => {

            formData.append(
                "resumes",
                file
            );

        }
    );


    setLoading(
        true
    );


    try {

        const response =
            await fetch(
                "/analyze",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail
                || "Analysis failed."
            );

        }


        displayResults(
            data
        );

    }
    catch (error) {

        showError(
            error.message
            || "Something went wrong."
        );

    }
    finally {

        setLoading(
            false
        );

    }

}


/* =========================================
   DISPLAY RESULTS
========================================= */


function displayResults(data) {

    resultsSection.classList.remove(
        "hidden"
    );


    document.getElementById(
        "resultSummary"
    ).textContent =
        `Analyzed ${data.successful_resumes}`
        + ` of ${data.total_resumes} resumes.`;


    renderSkills(
        "requiredSkills",
        data.required_skills
    );


    renderSkills(
        "preferredSkills",
        data.preferred_skills
    );


    renderCandidates(
        data.top_5
    );


    renderErrors(
        data.errors
    );


    resultsSection.scrollIntoView({
        behavior: "smooth"
    });

}


/* =========================================
   RENDER SKILLS
========================================= */


function renderSkills(
    elementId,
    skills
) {

    const element =
        document.getElementById(
            elementId
        );


    element.innerHTML = "";


    if (
        !skills ||
        skills.length === 0
    ) {

        element.innerHTML =
            "<span>No skills detected</span>";

        return;

    }


    skills.forEach(
        skill => {

            const span =
                document.createElement(
                    "span"
                );

            span.className =
                "skill";

            span.textContent =
                skill;

            element.appendChild(
                span
            );

        }
    );

}


/* =========================================
   RENDER CANDIDATES
========================================= */


function renderCandidates(
    candidates
) {

    const container =
        document.getElementById(
            "candidateList"
        );


    container.innerHTML = "";


    if (
        !candidates ||
        candidates.length === 0
    ) {

        container.innerHTML = `

            <div class="card">

                No candidates could
                be analyzed.

            </div>

        `;

        return;

    }


    candidates.forEach(
        candidate => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "candidate";


            const recommendationClass =
                getRecommendationClass(
                    candidate.recommendation
                );


            const matchedSkills =
                renderSkillText(
                    candidate.matched_skills,
                    "matched"
                );


            const missingSkills =
                renderSkillText(
                    candidate.missing_skills,
                    "missing"
                );


            const mandatoryWarning =
                candidate
                    .missing_mandatory
                    &&
                candidate
                    .missing_mandatory
                    .length > 0
                    ?

                `

                <div
                    class="mandatory-warning"
                >

                    <strong>
                        Missing mandatory
                        requirements:
                    </strong>

                    ${candidate
                        .missing_mandatory
                        .join(", ")}

                </div>

                `

                :

                "";


            card.innerHTML = `

                <div
                    class="candidate-top"
                >

                    <div>

                        <div>

                            <span
                                class="rank"
                            >
                                #${candidate.rank}
                            </span>

                        </div>

                        <div
                            class="candidate-name"
                            style="margin-top:10px"
                        >
                            ${escapeHtml(
                                candidate.filename
                            )}
                        </div>

                        <div
                            class="recommendation
                            ${recommendationClass}"
                        >
                            ${escapeHtml(
                                candidate.recommendation
                            )}
                        </div>

                    </div>


                    <div>

                        <div
                            class="score"
                        >
                            ${candidate.score}%
                        </div>

                        <small>
                            Overall Match
                        </small>

                    </div>

                </div>


                <div
                    class="score-grid"
                >

                    ${scoreBox(
                        "Skills",
                        candidate.skill_score
                    )}

                    ${scoreBox(
                        "Semantic",
                        candidate.semantic_score
                    )}

                    ${scoreBox(
                        "Experience",
                        candidate.experience_score
                    )}

                    ${scoreBox(
                        "Preferred",
                        candidate.preferred_score
                    )}

                    ${scoreBox(
                        "Education",
                        candidate.education_score
                    )}

                </div>


                <div
                    class="candidate-section"
                >

                    <h4>
                        Experience
                    </h4>

                    <p>
                        Candidate:
                        <strong>
                            ${candidate
                                .candidate_experience_years}
                            years
                        </strong>

                        &nbsp;|&nbsp;

                        Required:
                        <strong>
                            ${candidate
                                .required_experience_years}
                            years
                        </strong>
                    </p>

                </div>


                <div
                    class="candidate-section"
                >

                    <h4>
                        Matched Skills
                    </h4>

                    <div>
                        ${matchedSkills}
                    </div>

                </div>


                <div
                    class="candidate-section"
                >

                    <h4>
                        Missing Skills
                    </h4>

                    <div>
                        ${missingSkills}
                    </div>

                </div>


                ${mandatoryWarning}

            `;


            container.appendChild(
                card
            );

        }
    );

}


/* =========================================
   SCORE BOX
========================================= */


function scoreBox(
    label,
    value
) {

    return `

        <div class="score-box">

            <span class="label">
                ${label}
            </span>

            <span class="value">
                ${value}%
            </span>

        </div>

    `;

}


/* =========================================
   SKILL TEXT
========================================= */


function renderSkillText(
    skills,
    type
) {

    if (
        !skills ||
        skills.length === 0
    ) {

        return `
            <span class="${type}">
                None
            </span>
        `;

    }


    return `

        <span class="${type}">
            ${skills
                .map(
                    skill =>
                        escapeHtml(skill)
                )
                .join(", ")}
        </span>

    `;

}


/* =========================================
   RECOMMENDATION COLOR
========================================= */


function getRecommendationClass(
    recommendation
) {

    const value =
        recommendation
            .toLowerCase();


    if (
        value.includes(
            "excellent"
        )
    ) {

        return "excellent";

    }


    if (
        value.includes(
            "strong"
        )
    ) {

        return "strong";

    }


    if (
        value.includes(
            "good"
        )
    ) {

        return "good";

    }


    if (
        value.includes(
            "partial"
        )
    ) {

        return "partial";

    }


    return "weak";

}


/* =========================================
   LOADING
========================================= */


function setLoading(
    loadingState
) {

    if (loadingState) {

        loading.classList.remove(
            "hidden"
        );

        analyzeButton.disabled =
            true;

        analyzeButton.textContent =
            "Analyzing...";

    }
    else {

        loading.classList.add(
            "hidden"
        );

        analyzeButton.disabled =
            false;

        analyzeButton.textContent =
            "Analyze Resumes";

    }

}


/* =========================================
   ERRORS
========================================= */


function showError(
    message
) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "hidden"
    );

}


function clearError() {

    errorMessage.textContent = "";

    errorMessage.classList.add(
        "hidden"
    );

}


/* =========================================
   PROCESSING ERRORS
========================================= */


function renderErrors(
    errors
) {

    const container =
        document.getElementById(
            "processingErrors"
        );


    const list =
        document.getElementById(
            "errorList"
        );


    list.innerHTML = "";


    if (
        !errors ||
        errors.length === 0
    ) {

        container.classList.add(
            "hidden"
        );

        return;

    }


    errors.forEach(
        error => {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                error;

            list.appendChild(
                li
            );

        }
    );


    container.classList.remove(
        "hidden"
    );

}


/* =========================================
   FILE SIZE
========================================= */


function formatFileSize(
    bytes
) {

    if (bytes === 0) {

        return "0 Bytes";

    }


    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];


    const index =
        Math.floor(
            Math.log(bytes)
            / Math.log(1024)
        );


    return (
        parseFloat(
            (
                bytes
                / Math.pow(
                    1024,
                    index
                )
            ).toFixed(2)
        )
        + " "
        + units[index]
    );

}


/* =========================================
   HTML ESCAPING
========================================= */


function escapeHtml(
    value
) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        value;

    return div.innerHTML;

}

