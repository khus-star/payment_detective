import random
from datetime import datetime, timedelta

import pandas as pd


class PaymentDetective:
    """
    Payment Detective

    A prototype agentic-style investigation engine.

    It uses synthetic payment data and investigates a business problem
    by progressively narrowing down possible causes.
    """

    def __init__(self):
        self.df = self._make_data()

    # ---------------------------------------------------------
    # CREATE SYNTHETIC PAYMENT DATA
    # ---------------------------------------------------------

    def _make_data(self):

        random.seed(42)

        start = datetime(2026, 8, 31, 8, 0)

        rows = []

        banks = [
            "Bank A",
            "Bank B",
            "Bank X",
            "Bank C"
        ]

        methods = [
            "UPI",
            "Card",
            "Netbanking"
        ]

        cities = [
            "Bengaluru",
            "Mumbai",
            "Delhi",
            "Hyderabad",
            "Pune"
        ]

        devices = [
            "Android",
            "iOS",
            "Web"
        ]

        # Hidden incident begins here.
        incident_start = datetime(
            2026,
            9,
            1,
            14,
            20
        )

        for i in range(12000):

            timestamp = (
                start
                + timedelta(
                    minutes=random.randint(
                        0,
                        6 * 24 * 60 - 1
                    )
                )
            )

            method = random.choices(
                methods,
                weights=[55, 35, 10]
            )[0]

            bank = random.choice(banks)

            amount = random.randint(
                200,
                12000
            )

            city = random.choice(cities)

            device = random.choice(devices)

            # ---------------------------------------------
            # HIDDEN PAYMENT INCIDENT
            # ---------------------------------------------

            bad_route = (
                method == "UPI"
                and bank == "Bank X"
                and timestamp >= incident_start
            )

            # Normal success rates
            if method == "UPI":

                base_success = 0.94

            elif method == "Card":

                base_success = 0.96

            else:

                base_success = 0.92

            # Bank X + UPI suddenly becomes unhealthy.
            if bad_route:

                success_probability = 0.71

            else:

                success_probability = base_success

            success = (
                random.random()
                < success_probability
            )

            # Failure reason
            if success:

                failure = None

            else:

                failure = random.choice(
                    [
                        "BANK_DECLINE",
                        "TIMEOUT",
                        "NETWORK_ERROR",
                        "INSUFFICIENT_FUNDS"
                    ]
                )

            # Normal latency
            latency = random.randint(
                180,
                900
            )

            # Hidden incident also creates latency.
            if bad_route:

                latency = random.randint(
                    900,
                    2400
                )

            rows.append(
                {
                    "timestamp": timestamp,
                    "amount": amount,
                    "method": method,
                    "bank": bank,
                    "city": city,
                    "device": device,
                    "success": success,
                    "failure": failure,
                    "latency_ms": latency
                }
            )

        return pd.DataFrame(rows)

    # ---------------------------------------------------------
    # AVAILABLE CASES
    # ---------------------------------------------------------

    def cases(self):

        return [
            {
                "id": "revenue_drop",
                "name": "Revenue down 8%",
                "prompt": (
                    "Revenue is down 8% since Monday. "
                    "Find out why."
                )
            },
            {
                "id": "refund_spike",
                "name": "Refunds up 35%",
                "prompt": (
                    "Refunds have increased this week. "
                    "Investigate the cause."
                )
            }
        ]

    # ---------------------------------------------------------
    # HELPER
    # ---------------------------------------------------------

    def _rate(self, frame):

        if len(frame) == 0:

            return 0.0

        return float(
            frame["success"].mean()
        )

    # ---------------------------------------------------------
    # MAIN INVESTIGATION
    # ---------------------------------------------------------

    def investigate(self, case_id):

        if case_id == "refund_spike":

            return self._refund_case()

        # Copy dataset
        df = self.df.copy()

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        # Incident boundary
        cutoff = datetime(
            2026,
            9,
            1,
            14,
            20
        )

        # ---------------------------------------------
        # STEP 1
        # Compare before vs after
        # ---------------------------------------------

        before = df[
            df["timestamp"] < cutoff
        ]

        after = df[
            df["timestamp"] >= cutoff
        ]

        overall_before = self._rate(
            before
        )

        overall_after = self._rate(
            after
        )

        # ---------------------------------------------
        # STEP 2
        # Investigate payment methods
        # ---------------------------------------------

        method_rows = []

        for method, group in after.groupby(
            "method"
        ):

            before_group = before[
                before["method"] == method
            ]

            before_rate = self._rate(
                before_group
            )

            after_rate = self._rate(
                group
            )

            drop = (
                before_rate
                - after_rate
            ) * 100

            method_rows.append(
                {
                    "method": method,
                    "before": round(
                        before_rate * 100,
                        1
                    ),
                    "after": round(
                        after_rate * 100,
                        1
                    ),
                    "drop": round(
                        drop,
                        1
                    )
                }
            )

        method_rows.sort(
            key=lambda x: x["drop"],
            reverse=True
        )

        top_method = method_rows[0]["method"]

        # ---------------------------------------------
        # STEP 3
        # Investigate banks
        # ---------------------------------------------

        bank_rows = []

        method_after = after[
            after["method"] == top_method
        ]

        for bank, group in method_after.groupby(
            "bank"
        ):

            before_group = before[
                (before["method"] == top_method)
                &
                (before["bank"] == bank)
            ]

            before_rate = self._rate(
                before_group
            )

            after_rate = self._rate(
                group
            )

            drop = (
                before_rate
                - after_rate
            ) * 100

            bank_rows.append(
                {
                    "bank": bank,
                    "before": round(
                        before_rate * 100,
                        1
                    ),
                    "after": round(
                        after_rate * 100,
                        1
                    ),
                    "drop": round(
                        drop,
                        1
                    )
                }
            )

        bank_rows.sort(
            key=lambda x: x["drop"],
            reverse=True
        )

        top_bank = bank_rows[0]["bank"]

        # ---------------------------------------------
        # STEP 4
        # Investigate affected route
        # ---------------------------------------------

        route_after = after[
            (after["method"] == top_method)
            &
            (after["bank"] == top_bank)
        ]

        route_before = before[
            (before["method"] == top_method)
            &
            (before["bank"] == top_bank)
        ]

        # ---------------------------------------------
        # STEP 5
        # Investigate cities
        # ---------------------------------------------

        city_rows = []

        for city, group in route_after.groupby(
            "city"
        ):

            city_rows.append(
                {
                    "city": city,
                    "count": int(
                        len(group)
                    ),
                    "success": round(
                        self._rate(group) * 100,
                        1
                    )
                }
            )

        city_rows.sort(
            key=lambda x: x["count"],
            reverse=True
        )

        # ---------------------------------------------
        # STEP 6
        # Investigate latency
        # ---------------------------------------------

        if len(route_before) > 0:

            latency_before = int(
                route_before[
                    "latency_ms"
                ].median()
            )

        else:

            latency_before = 0

        if len(route_after) > 0:

            latency_after = int(
                route_after[
                    "latency_ms"
                ].median()
            )

        else:

            latency_after = 0

        # ---------------------------------------------
        # STEP 7
        # Confidence score
        # ---------------------------------------------

        confidence = 91

        if (
            latency_after
            > latency_before * 1.7
        ):

            confidence += 3

        if (
            len(route_before) > 0
            and len(route_after) > 0
            and
            route_after["success"].mean()
            <
            route_before["success"].mean()
            - 0.15
        ):

            confidence += 2

        confidence = min(
            confidence,
            99
        )

        # ---------------------------------------------
        # RETURN INVESTIGATION REPORT
        # ---------------------------------------------

        return {

            "case": "Revenue down 8%",

            "headline": (
                f"{top_bank} + {top_method} degradation "
                "is the strongest root-cause candidate."
            ),

            "confidence": confidence,

            "summary": {

                "revenue_change": "-8.2%",

                "success_before": round(
                    overall_before * 100,
                    1
                ),

                "success_after": round(
                    overall_after * 100,
                    1
                ),

                "top_method": top_method,

                "top_bank": top_bank,

                "latency_before": latency_before,

                "latency_after": latency_after
            },

            "timeline": [

                "Revenue anomaly detected",

                "Transaction volume checked — "
                "demand is stable",

                "Payment conversion identified "
                "as the driver",

                f"{top_method} isolated as "
                "the largest contributor",

                f"{top_bank} isolated as "
                "the highest-impact bank",

                "Temporal correlation confirmed "
                "from Monday 14:20",

                "Latency spike provides a "
                "second independent signal",

                "Root cause candidate established"
            ],

            "method_rows": method_rows,

            "bank_rows": bank_rows,

            "city_rows": city_rows,

            "evidence": [

                (
                    f"Overall success changed from "
                    f"{overall_before * 100:.1f}% to "
                    f"{overall_after * 100:.1f}%."
                ),

                (
                    f"{top_method} has the largest "
                    "conversion decline."
                ),

                (
                    f"{top_bank} has the largest decline "
                    f"inside {top_method}."
                ),

                (
                    f"Median route latency changed from "
                    f"{latency_before}ms to "
                    f"{latency_after}ms."
                ),

                (
                    "The degradation begins at a clear "
                    "time boundary rather than gradually."
                )
            ],

            "recommendation": (
                "Create an incident for the affected "
                "payment route and investigate or "
                "route around the degraded bank while "
                "the issue persists."
            ),

            "agent_tools": [

                "compare_revenue_periods()",

                "compare_transaction_volume()",

                "segment_by_payment_method()",

                "segment_by_bank()",

                "check_temporal_change_point()",

                "compare_route_latency()"
            ]
        }

    # ---------------------------------------------------------
    # SECOND DEMO CASE
    # ---------------------------------------------------------

    def _refund_case(self):

        return {

            "case": "Refunds up 35%",

            "headline": (
                "Simulated investigation: refund spike "
                "concentrated in one merchant segment."
            ),

            "confidence": 84,

            "summary": {

                "revenue_change": "-3.4%",

                "success_before": 95.1,

                "success_after": 93.8,

                "top_method": "Card",

                "top_bank": "Bank B",

                "latency_before": 420,

                "latency_after": 430
            },

            "timeline": [

                "Refund anomaly detected",

                "Refunds segmented by merchant category",

                "One category shows abnormal concentration",

                "Top merchants compared against baseline",

                "Spike is concentrated rather than "
                "platform-wide",

                "Case recommended for merchant-level review"
            ],

            "method_rows": [

                {
                    "method": "Card",
                    "before": 96.0,
                    "after": 94.1,
                    "drop": 1.9
                },

                {
                    "method": "UPI",
                    "before": 94.4,
                    "after": 93.7,
                    "drop": 0.7
                },

                {
                    "method": "Netbanking",
                    "before": 92.3,
                    "after": 92.0,
                    "drop": 0.3
                }
            ],

            "bank_rows": [

                {
                    "bank": "Bank B",
                    "before": 95.7,
                    "after": 93.2,
                    "drop": 2.5
                },

                {
                    "bank": "Bank A",
                    "before": 95.4,
                    "after": 94.0,
                    "drop": 1.4
                },

                {
                    "bank": "Bank X",
                    "before": 95.2,
                    "after": 94.8,
                    "drop": 0.4
                }
            ],

            "city_rows": [],

            "evidence": [

                "The spike is concentrated rather than "
                "evenly distributed.",

                "Card transactions show the largest "
                "conversion movement.",

                "One bank segment is disproportionately "
                "affected.",

                "The pattern is suitable for "
                "merchant-level investigation."
            ],

            "recommendation": (
                "Create a review case for the affected "
                "merchant segment and inspect recent "
                "product, refund-policy, and campaign changes."
            ),

            "agent_tools": [

                "detect_refund_anomaly()",

                "segment_by_merchant()",

                "compare_payment_methods()",

                "compare_banks()",

                "check_recent_changes()"
            ]
        }