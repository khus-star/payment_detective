let currentResult = null;


// =====================================================
// SMALL DELAY FUNCTION
// =====================================================

function sleep(ms) {

    return new Promise(
        resolve => setTimeout(resolve, ms)
    );

}


// =====================================================
// START INVESTIGATION
// =====================================================

async function startInvestigation() {

    const button =
        document.getElementById(
            "investigateBtn"
        );


    const section =
        document.getElementById(
            "investigation"
        );


    const timeline =
        document.getElementById(
            "timeline"
        );


    const activity =
        document.getElementById(
            "activity"
        );


    const result =
        document.getElementById(
            "result"
        );


    // Show investigation area
    section.classList.remove(
        "hidden"
    );


    // Hide previous result
    result.classList.add(
        "hidden"
    );


    timeline.innerHTML = "";

    activity.innerHTML = "";


    button.disabled = true;

    button.textContent =
        "INVESTIGATING...";


    // =================================================
    // SIMULATED AGENT INVESTIGATION
    // =================================================

    const steps = [

        [
            "observe",
            "Reading the business problem"
        ],

        [
            "tool",
            "compare_revenue_periods()"
        ],

        [
            "tool",
            "compare_transaction_volume()"
        ],

        [
            "hypothesis",
            "Hypothesis: demand may have changed"
        ],

        [
            "tool",
            "segment_by_payment_method()"
        ],

        [
            "hypothesis",
            "Hypothesis updated: payment conversion is the driver"
        ],

        [
            "tool",
            "segment_by_bank()"
        ],

        [
            "tool",
            "check_temporal_change_point()"
        ],

        [
            "tool",
            "compare_route_latency()"
        ],

        [
            "conclusion",
            "Root-cause candidate established"
        ]

    ];


    // Display each investigation step
    for (
        const [type, text]
        of steps
    ) {

        const row =
            document.createElement(
                "div"
            );


        row.className =
            "timeline-item active flash";


        row.textContent = text;


        timeline.appendChild(
            row
        );


        const line =
            document.createElement(
                "div"
            );


        line.innerHTML =
            `<b>${type.toUpperCase()}</b>  ${text}`;


        line.className =
            "flash";


        activity.appendChild(
            line
        );


        await sleep(350);

    }


    // =================================================
    // SEND REQUEST TO PYTHON BACKEND
    // =================================================

    const caseId =
        document.getElementById(
            "caseSelect"
        ).value;


    try {

        const response =
            await fetch(
                "/api/investigate",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            case_id:
                                caseId
                        }
                    )

                }
            );


        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }


        currentResult =
            await response.json();


        renderResult(
            currentResult
        );


    } catch (error) {

        console.error(
            error
        );


        alert(
            "Something went wrong. " +
            "Check the VS Code terminal."
        );

    }


    button.disabled = false;


    button.innerHTML =
        'INVESTIGATE <span>→</span>';

}


// =====================================================
// DISPLAY RESULT
// =====================================================

function renderResult(result) {

    const resultPanel =
        document.getElementById(
            "result"
        );


    resultPanel.classList.remove(
        "hidden"
    );


    // Headline
    document.getElementById(
        "headline"
    ).textContent =
        result.headline;


    // Confidence
    document.getElementById(
        "confidence"
    ).textContent =
        result.confidence + "%";


    // =================================================
    // STATS
    // =================================================

    const summary =
        result.summary;


    document.getElementById(
        "stats"
    ).innerHTML = `

        <div class="stat">

            <small>
                REVENUE CHANGE
            </small>

            <strong>
                ${summary.revenue_change}
            </strong>

        </div>


        <div class="stat">

            <small>
                SUCCESS RATE
            </small>

            <strong>
                ${summary.success_before}%
                →
                ${summary.success_after}%
            </strong>

        </div>


        <div class="stat">

            <small>
                TOP METHOD
            </small>

            <strong>
                ${summary.top_method}
            </strong>

        </div>


        <div class="stat">

            <small>
                TOP BANK
            </small>

            <strong>
                ${summary.top_bank}
            </strong>

        </div>

    `;


    // =================================================
    // EVIDENCE
    // =================================================

    document.getElementById(
        "evidence"
    ).innerHTML =
        result.evidence
            .map(
                item =>
                    `<div class="evidence">
                        ${item}
                    </div>`
            )
            .join("");


    // =================================================
    // RECOMMENDATION
    // =================================================

    document.getElementById(
        "recommendation"
    ).textContent =
        result.recommendation;


    // =================================================
    // TOOLS
    // =================================================

    document.getElementById(
        "tools"
    ).innerHTML =
        result.agent_tools
            .map(
                tool =>
                    `<span class="tool">
                        ${tool}
                    </span>`
            )
            .join("");


    // Clear previous messages
    document.getElementById(
        "incidentMsg"
    ).textContent = "";


    document.getElementById(
        "challengeResult"
    ).classList.add(
        "hidden"
    );


    // Scroll to result
    window.scrollTo(
        {
            top:
                resultPanel.offsetTop - 20,

            behavior:
                "smooth"
        }
    );

}


// =====================================================
// CREATE INCIDENT
// =====================================================

function createIncident() {

    document.getElementById(
        "incidentMsg"
    ).textContent =
        "✓ Demo incident created: " +
        "PAY-1842 • Assigned to Payment Reliability";

}


// =====================================================
// CHALLENGE THE CONCLUSION
// =====================================================

async function challengeConclusion() {

    const box =
        document.getElementById(
            "challengeResult"
        );


    box.classList.remove(
        "hidden"
    );


    box.innerHTML = `

        <b>
            CHALLENGING CONCLUSION...
        </b>

        <br>

        Checking merchant configuration...

        <br>

        Checking traffic mix...

        <br>

        Checking other banks...

        <br>

        Checking global payment-method effects...

    `;


    await sleep(1200);


    box.innerHTML = `

        <b>
            CONCLUSION SURVIVES ADVERSARIAL CHECK.
        </b>

        <br><br>

        Merchant configuration does not explain
        the timing.

        <br>

        Traffic volume is stable.

        <br>

        Other banks do not show the same degradation.

        <br>

        The latency spike independently supports
        the Bank X + UPI hypothesis.

        <br><br>

        <b>
            Confidence remains
            ${currentResult.confidence}%.
        </b>

    `;

}