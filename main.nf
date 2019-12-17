log.info "* Project dir:        ${workflow.projectDir}"
log.info "* Launch dir:         ${workflow.launchDir}"
log.info "* Work dir:           ${workflow.workDir.toUriString()}"

num = Channel.from( 1, 2, 3 )

process make_file {
    echo true

    input:
    val x from num


    script:
    output_file = "${x}.txt"
    """
    touch "${output_file}"
    record.py --key "input_val" --value "${x}" --type "val"
    record.py --key "output_file" --value "${output_file}" --type "file"
    """
} // "the id is:" "${id}" "${task}" "${task.cpus}" "${this.workDir}"
