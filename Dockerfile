FROM slalomggp/dataops:latest-dev

RUN pwd && ls -la

RUN s-tap install target-csv
# RUN s-tap install tap-rest-api .
