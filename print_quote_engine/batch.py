"""Portable, order-preserving batch quote orchestration."""

from .calculator import calculate


MAX_BATCH_ITEMS = 50


def calculate_batch(items, policy):
    """Calculate independent quotes and keep item-level failures isolated.

    Persistence and idempotency belong to the host application.  This helper is
    intentionally deterministic and retains the input order so a UI can map
    every result back to its source file.
    """
    items=list(items)
    if not 1 <= len(items) <= MAX_BATCH_ITEMS:
        raise ValueError('BATCH_SIZE_OUT_OF_RANGE')
    rows=[]
    for index,item in enumerate(items):
        try:
            rows.append({'index':index,'status':'SUCCEEDED','result':calculate(item,policy)})
        except ValueError as exc:
            rows.append({'index':index,'status':'FAILED','error_code':str(exc)})
    succeeded=sum(row['status']=='SUCCEEDED' for row in rows)
    return {'requested':len(rows),'succeeded':succeeded,'failed':len(rows)-succeeded,'items':rows}
