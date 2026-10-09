# Arb certificate CSV line-ending repair

The first complete v3 replay reached the Git staging check after the
authoritative certificates and adversarial controls had run.  Git then
reported every generated CSV record as trailing whitespace.  The records were
not mathematically malformed: Python's standard `csv` dialect writes CRLF by
default, even when the file is opened with `newline=""`.  The carriage return
was displayed as `^M` and was treated by `git diff --check` as trailing
whitespace.

The certifier now sets `lineterminator="\n"` explicitly for every CSV writer.
The replay runner also scans every generated CSV byte-for-byte and refuses to
continue if any carriage return remains.  This change affects serialization
only; it does not alter formulas, interval enclosures, partitions, or theorem
targets.
