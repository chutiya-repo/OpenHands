const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('wsai_code-hello-world.helloWorld', function () {
        vscode.window.showInformationMessage('Hello from WSAI CODE!');
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
