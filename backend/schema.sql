-- The PANTRY shelf: one table called "calls".
-- Think of it as an Excel sheet: each row is one call, each column is one detail.
-- "IF NOT EXISTS" means: create it the first time, and do nothing after that.

CREATE TABLE IF NOT EXISTS calls (
    id         SERIAL PRIMARY KEY,                 -- the row's unique number: 1, 2, 3... filled in automatically
    caller     TEXT NOT NULL,                      -- who called, e.g. 'Asha'
    summary    TEXT NOT NULL,                      -- what the call was about, e.g. 'Wants a loan'
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()  -- when it was saved, filled in automatically
);
