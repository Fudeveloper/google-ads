from __future__ import annotations


PAYOUT_EVENT_POINTS = {
    "booked": 2,
    "confirmed": 4,
    "showed": 8,
    "completed": 10,
    "approved": 10,
    "paid": 12,
}

CAPACITY_POINTS = {
    "missing": 0,
    "unknown": 0,
    "constrained": 3,
    "adequate": 8,
    "open": 10,
}

TIMEZONE_POINTS = {
    "missing": 0,
    "unclear": 2,
    "buyer_local": 5,
    "user_local": 8,
    "aligned": 10,
}

REMINDER_CONSENT_POINTS = {
    "missing": 0,
    "generic": 3,
    "email_only": 5,
    "channel_specific": 10,
    "opted_out": 0,
}

CONFIRMATION_POINTS = {
    "missing": 0,
    "manual": 4,
    "automated": 7,
    "confirmed_workflow": 10,
}

BUYER_TERMS_POINTS = {
    "missing": 0,
    "draft": 2,
    "received": 5,
    "approved": 10,
}


def calculate_appointment_lead_review(
    *,
    payout_event: str,
    payout_amount: float,
    estimated_cpc: float,
    click_to_request_rate_percent: float,
    request_to_book_rate_percent: float,
    confirmation_rate_percent: float,
    show_rate_percent: float,
    completed_rate_percent: float,
    paid_rate_percent: float,
    cancel_rate_percent: float,
    no_show_rate_percent: float,
    duplicate_booking_rate_percent: float,
    reschedule_rate_percent: float,
    reminder_cost_per_booking: float,
    no_show_cost_per_booking: float,
    available_slots: float,
    expected_bookings: float,
    lead_age_hours: int,
    slot_delay_hours: int,
    calendar_capacity_status: str,
    timezone_status: str,
    reminder_consent_status: str,
    confirmation_process_status: str,
    buyer_terms_status: str,
    payout_definition_clear: bool,
    duplicate_window_defined: bool,
    no_show_reason_map_ready: bool,
    calendar_capacity_evidence: bool,
    reminder_template_reviewed: bool,
    offline_conversion_mapping_ready: bool,
    human_review: bool,
) -> dict[str, object]:
    click_to_request_rate = _rate(click_to_request_rate_percent)
    request_to_book_rate = _rate(request_to_book_rate_percent)
    confirmation_rate = _rate(confirmation_rate_percent)
    show_rate = _rate(show_rate_percent)
    completed_rate = _rate(completed_rate_percent)
    paid_rate = _rate(paid_rate_percent)
    cancel_rate = _rate(cancel_rate_percent)
    no_show_rate = _rate(no_show_rate_percent)
    duplicate_booking_rate = _rate(duplicate_booking_rate_percent)
    retained_rate = max(1 - cancel_rate - duplicate_booking_rate, 0)

    expected_value_per_booking = (
        payout_amount
        * confirmation_rate
        * show_rate
        * completed_rate
        * paid_rate
        * retained_rate
    )
    expected_value_per_click = (
        click_to_request_rate * request_to_book_rate * expected_value_per_booking
    )
    expected_booking_cost_per_click = (
        click_to_request_rate
        * request_to_book_rate
        * (reminder_cost_per_booking + no_show_cost_per_booking * no_show_rate)
    )
    safe_cpc = expected_value_per_click * 0.65 - expected_booking_cost_per_click
    cpc_margin_percent = _margin_percent(safe_cpc, estimated_cpc)
    safe_appointment_spend = max(
        available_slots - expected_bookings, 0
    ) * expected_value_per_booking * 0.60

    blockers = _blockers(
        payout_event=payout_event,
        payout_amount=payout_amount,
        estimated_cpc=estimated_cpc,
        click_to_request_rate_percent=click_to_request_rate_percent,
        request_to_book_rate_percent=request_to_book_rate_percent,
        confirmation_rate_percent=confirmation_rate_percent,
        show_rate_percent=show_rate_percent,
        completed_rate_percent=completed_rate_percent,
        paid_rate_percent=paid_rate_percent,
        cancel_rate_percent=cancel_rate_percent,
        no_show_rate_percent=no_show_rate_percent,
        duplicate_booking_rate_percent=duplicate_booking_rate_percent,
        reschedule_rate_percent=reschedule_rate_percent,
        safe_cpc=safe_cpc,
        available_slots=available_slots,
        expected_bookings=expected_bookings,
        lead_age_hours=lead_age_hours,
        slot_delay_hours=slot_delay_hours,
        calendar_capacity_status=calendar_capacity_status,
        timezone_status=timezone_status,
        reminder_consent_status=reminder_consent_status,
        confirmation_process_status=confirmation_process_status,
        buyer_terms_status=buyer_terms_status,
        payout_definition_clear=payout_definition_clear,
        duplicate_window_defined=duplicate_window_defined,
        no_show_reason_map_ready=no_show_reason_map_ready,
        calendar_capacity_evidence=calendar_capacity_evidence,
        reminder_template_reviewed=reminder_template_reviewed,
        offline_conversion_mapping_ready=offline_conversion_mapping_ready,
        human_review=human_review,
    )

    score = 0
    score += PAYOUT_EVENT_POINTS.get(payout_event, 0)
    score += _economics_points(
        expected_value_per_click=expected_value_per_click,
        safe_cpc=safe_cpc,
        estimated_cpc=estimated_cpc,
    )
    score += _funnel_points(
        click_to_request_rate_percent=click_to_request_rate_percent,
        request_to_book_rate_percent=request_to_book_rate_percent,
        confirmation_rate_percent=confirmation_rate_percent,
        show_rate_percent=show_rate_percent,
        completed_rate_percent=completed_rate_percent,
        paid_rate_percent=paid_rate_percent,
        cancel_rate_percent=cancel_rate_percent,
        no_show_rate_percent=no_show_rate_percent,
        duplicate_booking_rate_percent=duplicate_booking_rate_percent,
    )
    score += _freshness_points(lead_age_hours, slot_delay_hours)
    score += _slot_points(available_slots, expected_bookings)
    score += CAPACITY_POINTS.get(calendar_capacity_status, 0)
    score += TIMEZONE_POINTS.get(timezone_status, 0)
    score += REMINDER_CONSENT_POINTS.get(reminder_consent_status, 0)
    score += CONFIRMATION_POINTS.get(confirmation_process_status, 0)
    score += BUYER_TERMS_POINTS.get(buyer_terms_status, 0)
    score += 5 if payout_definition_clear else 0
    score += 4 if duplicate_window_defined else 0
    score += 5 if no_show_reason_map_ready else 0
    score += 5 if calendar_capacity_evidence else 0
    score += 5 if reminder_template_reviewed else 0
    score += 5 if offline_conversion_mapping_ready else 0
    score += 5 if human_review else 0
    score = max(min(score, 100), 0)

    return {
        "score": score,
        "risk_level": _risk_level(
            score=score,
            blockers=blockers,
            calendar_capacity_status=calendar_capacity_status,
            reminder_consent_status=reminder_consent_status,
            payout_event=payout_event,
        ),
        "recommended_action": _recommended_action(
            score=score,
            blockers=blockers,
            safe_cpc=safe_cpc,
            estimated_cpc=estimated_cpc,
            calendar_capacity_status=calendar_capacity_status,
            reminder_consent_status=reminder_consent_status,
            buyer_terms_status=buyer_terms_status,
            no_show_rate_percent=no_show_rate_percent,
        ),
        "expected_value_per_booking": round(expected_value_per_booking, 4),
        "expected_value_per_click": round(expected_value_per_click, 4),
        "safe_cpc": round(safe_cpc, 4),
        "cpc_margin_percent": round(cpc_margin_percent, 2),
        "safe_appointment_spend": round(safe_appointment_spend, 2),
        "blockers": blockers,
    }


def _rate(value: float) -> float:
    return max(min(value / 100, 1), 0)


def _margin_percent(safe_cpc: float, estimated_cpc: float) -> float:
    if estimated_cpc <= 0:
        return 0
    return (safe_cpc - estimated_cpc) / estimated_cpc * 100


def _economics_points(
    *,
    expected_value_per_click: float,
    safe_cpc: float,
    estimated_cpc: float,
) -> int:
    if expected_value_per_click <= 0:
        return 0
    if estimated_cpc <= 0:
        return 5
    if safe_cpc >= estimated_cpc * 1.4:
        return 15
    if safe_cpc >= estimated_cpc:
        return 10
    if safe_cpc >= estimated_cpc * 0.75:
        return 5
    return 2


def _funnel_points(
    *,
    click_to_request_rate_percent: float,
    request_to_book_rate_percent: float,
    confirmation_rate_percent: float,
    show_rate_percent: float,
    completed_rate_percent: float,
    paid_rate_percent: float,
    cancel_rate_percent: float,
    no_show_rate_percent: float,
    duplicate_booking_rate_percent: float,
) -> int:
    if (
        click_to_request_rate_percent >= 5
        and request_to_book_rate_percent >= 70
        and confirmation_rate_percent >= 80
        and show_rate_percent >= 70
        and completed_rate_percent >= 65
        and paid_rate_percent >= 55
        and cancel_rate_percent <= 10
        and no_show_rate_percent <= 15
        and duplicate_booking_rate_percent <= 3
    ):
        return 18
    if (
        click_to_request_rate_percent >= 2
        and request_to_book_rate_percent >= 50
        and confirmation_rate_percent >= 60
        and show_rate_percent >= 50
        and completed_rate_percent >= 45
        and paid_rate_percent >= 35
        and cancel_rate_percent <= 20
        and no_show_rate_percent <= 30
        and duplicate_booking_rate_percent <= 8
    ):
        return 10
    if click_to_request_rate_percent > 0 and request_to_book_rate_percent > 0:
        return 4
    return 0


def _freshness_points(lead_age_hours: int, slot_delay_hours: int) -> int:
    points = 0
    if lead_age_hours <= 2:
        points += 5
    elif lead_age_hours <= 24:
        points += 3
    if slot_delay_hours <= 24:
        points += 5
    elif slot_delay_hours <= 72:
        points += 3
    return points


def _slot_points(available_slots: float, expected_bookings: float) -> int:
    if available_slots <= 0:
        return 0
    if expected_bookings <= available_slots * 0.70:
        return 8
    if expected_bookings <= available_slots:
        return 4
    return 0


def _risk_level(
    *,
    score: int,
    blockers: list[str],
    calendar_capacity_status: str,
    reminder_consent_status: str,
    payout_event: str,
) -> str:
    if calendar_capacity_status in {"missing", "unknown"}:
        return "high"
    if reminder_consent_status in {"missing", "opted_out"}:
        return "high"
    if payout_event in {"booked", "confirmed"} and blockers:
        return "high"
    if score >= 85 and not blockers:
        return "low"
    if score >= 65:
        return "medium"
    return "high"


def _recommended_action(
    *,
    score: int,
    blockers: list[str],
    safe_cpc: float,
    estimated_cpc: float,
    calendar_capacity_status: str,
    reminder_consent_status: str,
    buyer_terms_status: str,
    no_show_rate_percent: float,
) -> str:
    if calendar_capacity_status in {"missing", "unknown"}:
        return "hold_for_calendar_capacity"
    if reminder_consent_status in {"missing", "opted_out"}:
        return "fix_reminder_consent"
    if buyer_terms_status in {"missing", "draft"}:
        return "hold_for_buyer_terms"
    if no_show_rate_percent > 30:
        return "pause_and_fix_no_show"
    if safe_cpc <= 0 or (estimated_cpc > 0 and safe_cpc < estimated_cpc):
        return "rework_booking_economics"
    if blockers:
        return "calendar_and_reminder_review"
    if score >= 85:
        return "approve_manual_test"
    if score >= 70:
        return "small_test_only"
    return "hold_for_booking_rework"


def _blockers(
    *,
    payout_event: str,
    payout_amount: float,
    estimated_cpc: float,
    click_to_request_rate_percent: float,
    request_to_book_rate_percent: float,
    confirmation_rate_percent: float,
    show_rate_percent: float,
    completed_rate_percent: float,
    paid_rate_percent: float,
    cancel_rate_percent: float,
    no_show_rate_percent: float,
    duplicate_booking_rate_percent: float,
    reschedule_rate_percent: float,
    safe_cpc: float,
    available_slots: float,
    expected_bookings: float,
    lead_age_hours: int,
    slot_delay_hours: int,
    calendar_capacity_status: str,
    timezone_status: str,
    reminder_consent_status: str,
    confirmation_process_status: str,
    buyer_terms_status: str,
    payout_definition_clear: bool,
    duplicate_window_defined: bool,
    no_show_reason_map_ready: bool,
    calendar_capacity_evidence: bool,
    reminder_template_reviewed: bool,
    offline_conversion_mapping_ready: bool,
    human_review: bool,
) -> list[str]:
    blockers: list[str] = []
    if payout_event not in PAYOUT_EVENT_POINTS:
        blockers.append("payout event is not mapped")
    if payout_event in {"booked", "confirmed"}:
        blockers.append("payout event is earlier than showed or paid")
    if payout_amount <= 0:
        blockers.append("appointment payout is missing")
    if click_to_request_rate_percent <= 0:
        blockers.append("click-to-request rate is missing")
    if request_to_book_rate_percent < 50:
        blockers.append("request-to-book rate is below 50 percent")
    if confirmation_rate_percent < 60:
        blockers.append("confirmation rate is below 60 percent")
    if show_rate_percent < 50:
        blockers.append("show rate is below 50 percent")
    if completed_rate_percent < 45:
        blockers.append("completed consult or service rate is below 45 percent")
    if paid_rate_percent < 35:
        blockers.append("paid rate is below 35 percent")
    if cancel_rate_percent > 20:
        blockers.append("cancel rate exceeds 20 percent")
    if no_show_rate_percent > 30:
        blockers.append("no-show rate exceeds 30 percent")
    if duplicate_booking_rate_percent > 8:
        blockers.append("duplicate booking rate exceeds 8 percent")
    if reschedule_rate_percent > 30:
        blockers.append("reschedule rate exceeds 30 percent")
    if estimated_cpc > 0 and safe_cpc < estimated_cpc:
        blockers.append("safe CPC is below estimated CPC")
    if safe_cpc <= 0:
        blockers.append("safe CPC is zero or negative after no-show and reminder cost")
    if available_slots <= 0:
        blockers.append("available appointment slots are missing")
    elif expected_bookings > available_slots:
        blockers.append("expected bookings exceed available slots")
    if lead_age_hours > 24:
        blockers.append("lead age is older than 24 hours before booking")
    if slot_delay_hours > 72:
        blockers.append("slot delay is longer than 72 hours")
    if calendar_capacity_status in {"missing", "unknown", "constrained"}:
        blockers.append("calendar capacity is not ready for scaling")
    if timezone_status in {"missing", "unclear"}:
        blockers.append("slot timezone is missing or unclear")
    if reminder_consent_status in {"missing", "generic", "opted_out"}:
        blockers.append("reminder consent is not channel-specific")
    if confirmation_process_status == "missing":
        blockers.append("confirmation workflow is missing")
    if buyer_terms_status in {"missing", "draft"}:
        blockers.append("buyer appointment terms are not approved")
    if not payout_definition_clear:
        blockers.append("payout, show, no-show and cancel definitions are not clear")
    if not duplicate_window_defined:
        blockers.append("duplicate booking window is missing")
    if not no_show_reason_map_ready:
        blockers.append("no-show reason map is missing")
    if not calendar_capacity_evidence:
        blockers.append("calendar capacity evidence is missing")
    if not reminder_template_reviewed:
        blockers.append("reminder template review is missing")
    if not offline_conversion_mapping_ready:
        blockers.append("showed/paid offline conversion mapping is missing")
    if not human_review:
        blockers.append("human review is missing")
    return blockers
