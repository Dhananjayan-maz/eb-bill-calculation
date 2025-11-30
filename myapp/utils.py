# # myapp/utils.py
# from datetime import date
# import calendar

# def compute_billing_period_for_date(ref_date: date, cycle_day: int = 15):
#     # simple cycle: if ref_date.day >= cycle_day -> start = cycle_day this month, end = cycle_day next month
#     year = ref_date.year
#     month = ref_date.month
#     if ref_date.day >= cycle_day:
#         start_year, start_month = year, month
#         if month == 12:
#             end_year, end_month = year + 1, 1
#         else:
#             end_year, end_month = year, month + 1
#     else:
#         if month == 1:
#             start_year, start_month = year - 1, 12
#         else:
#             start_year, start_month = year, month - 1
#         end_year, end_month = year, month

#     start_day = min(cycle_day, calendar.monthrange(start_year, start_month)[1])
#     end_day = min(cycle_day, calendar.monthrange(end_year, end_month)[1])

#     from datetime import date
#     start = date(start_year, start_month, start_day)
#     end = date(end_year, end_month, end_day)
#     return start, end

# myapp/utils.py
from datetime import date
import calendar

def compute_billing_period_for_date(ref_date: date, cycle_day: int = 15):
    """
    Return (period_start, period_end) where:
      - period_end is the most recent cycle_day date that is <= ref_date
      - period_start is the same cycle_day in the previous month to period_end

    Examples (cycle_day=15):
      ref_date 2025-11-16 -> (2025-10-15, 2025-11-15)
      ref_date 2025-11-15 -> (2025-10-15, 2025-11-15)
      ref_date 2025-11-14 -> (2025-09-15, 2025-10-15)
    """
    year = ref_date.year
    month = ref_date.month

    # candidate = cycle_day clamped to this month
    last_day_this_month = calendar.monthrange(year, month)[1]
    candidate_day = min(cycle_day, last_day_this_month)
    candidate = date(year, month, candidate_day)

    if candidate <= ref_date:
        end_year, end_month, end_day = candidate.year, candidate.month, candidate.day
    else:
        # use previous month as period_end
        if month == 1:
            end_year, end_month = year - 1, 12
        else:
            end_year, end_month = year, month - 1
        last_day_prev = calendar.monthrange(end_year, end_month)[1]
        end_day = min(cycle_day, last_day_prev)

    period_end = date(end_year, end_month, end_day)

    # period_start = cycle_day of the month before period_end
    if period_end.month == 1:
        start_year, start_month = period_end.year - 1, 12
    else:
        start_year, start_month = period_end.year, period_end.month - 1
    last_day_start = calendar.monthrange(start_year, start_month)[1]
    start_day = min(cycle_day, last_day_start)
    period_start = date(start_year, start_month, start_day)

    return period_start, period_end
