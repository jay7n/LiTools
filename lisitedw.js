#!/usr/local/bin/node

// This is very important for global module locating
module.paths.push('/usr/local/lib/node_modules/')

const parseArgs = require('minimist')
const chalk = require('chalk')
const fs = require('fs')
const {
    exec,
    execSync,
} = require('child_process');

function _collect_urls(file_content) {
    const list = []
    const regexp = /curl\s+'(.+?)'/g
    let match = null

    while (match = regexp.exec(file_content)) {
        list.push(match[1])
    }
    return list
}

function _pre_deco_urls(urls) {
    const deco_urls = urls.map(url => {
        const filtered_url = url.match(/^(.+?)\?t=.+$/)
        url = filtered_url ? filtered_url[1] : url
        if (url.match(/\/$/)) {
            // this is probably a index.html page
            url = url + 'index.html'
        }
        return url
    })
    return deco_urls
}

function _deco_urls_with_wget_cmd(urls) {
    const wget_prefix = 'wget -x '
    const deco_urls = urls.map(url => {
        return wget_prefix + url
    })
    return deco_urls
}

function _exec_wget_cmds(cmds) {
    cmds.map(cmd => {
        try {
            console.log(chalk.cyan('executing: ' + cmd))
            const stdout = execSync(cmd)
            console.log(`stdout: ${stdout}`)
            console.log(chalk.green('done'))
        } catch(err) {
            console.log(chalk.red(err))
        }
    })
}



function main(args) {
    const script_filename = args['script-filename']
    const data = fs.readFileSync(script_filename, 'utf-8')
    let list = _collect_urls(data)
    list = _pre_deco_urls(list)
    list = _deco_urls_with_wget_cmd(list)
    _exec_wget_cmds(list)
}

if (require.main === module) {
    const args = parseArgs(process.argv.slice(2))
    main(args)
} else {
    module.exports = main
}
