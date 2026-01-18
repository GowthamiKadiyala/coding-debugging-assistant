import * as vscode from "vscode";
import axios from "axios"; // We need to install this later

export function activate(context: vscode.ExtensionContext) {
  console.log(
    'Congratulations, your extension "debug-assistant-client" is active!',
  );

  // Command 1: "Ask AI Debugger"
  let disposable = vscode.commands.registerCommand(
    "debug-assistant.askAI",
    async () => {
      // 1. Get the Active Editor
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showErrorMessage("No active editor found!");
        return;
      }

      // 2. Get Selected Code (Context)
      const selection = editor.selection;
      const selectedCode = editor.document.getText(selection);

      // 3. Ask User for the Error Message
      const errorMessage = await vscode.window.showInputBox({
        placeHolder: "Describe the error (or paste stack trace)...",
      });

      if (!errorMessage) return; // User cancelled

      // 4. Show "Thinking..." Notification
      vscode.window.withProgress(
        {
          location: vscode.ProgressLocation.Notification,
          title: "AI is analyzing your code...",
          cancellable: false,
        },
        async (progress) => {
          try {
            // 5. Call your Python Backend
            // Note: Ensure your backend is running on port 8000!
            const response = await axios.post("http://localhost:8000/debug", {
              error_message: errorMessage,
              selected_code: selectedCode || "No code selected",
            });

            // 6. Show Result (Senior UX: Open in a new text document)
            const analysis = response.data.analysis;
            const doc = await vscode.workspace.openTextDocument({
              content: analysis,
              language: "markdown",
            });
            await vscode.window.showTextDocument(doc, {
              viewColumn: vscode.ViewColumn.Beside,
            });
          } catch (error) {
            vscode.window.showErrorMessage(`AI Backend Failed: ${error}`);
          }
        },
      );
    },
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {}
