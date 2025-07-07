#/bin/bash

make evaluations
cat reports/classification-report.txt
uvicorn app.api:app --host "0.0.0.0"