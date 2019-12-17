#!/usr/bin/env python
from flask import Flask, request, jsonify
import os
import json
"""
Flask server for recieving http POST messages from Nextflow pipeline
and checking them for the presence of a communicator.json file at the specified location
and then loading the communicator data if present, for later usage (e.g. passing to an API endpoint)
"""
app = Flask(__name__)

communicator_file = "communicator.json"

@app.route('/', methods=['POST'])
def entry_point():
    data = request.json
    print(data.keys())
    runId = data['runId']
    runName = data['runName']
    utcTime = data['utcTime']

    # stash a copy of the JSON from the POST message for later viewing
    # warning: filename has ':' in it from timestamp so dont try to view it in NTFS filesystem
    output_json = "{}.{}.{}.json".format(runId, runName, utcTime)
    output_json_dir = "json"
    output_json_path = os.path.join(output_json_dir, output_json)
    with open(output_json_path, "w") as fout:
        json.dump(data, fout, indent = 4)

    print("""
[{utcTime}] [{runId}] [{runName}]
    """.format(
    runId = runId, runName = runName, utcTime = utcTime
    ))

    # check if its a pipeline task; has 'trace' key
    # pipeline start/complete events have 'metadata' key instead
    if 'trace' in data:
        trace = data.pop('trace')
        workdir = trace['workdir']
        process = trace['process']
        task_name = trace['name']
        communicator_filepath = os.path.join(workdir, communicator_file)

        print(
        """
process: {process} ({task_name})
trace: {trace}
workdir: {workdir}""".format(
        trace = trace, workdir = workdir, process = process, task_name = task_name
        ))

        # if there is a communicator file present, load the data
        if os.path.exists(communicator_filepath):
            communicator_data = json.load(open(communicator_filepath))
            print("""communicator_data: {communicator_data}
            """.format(
            communicator_data = communicator_data
            ))

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
