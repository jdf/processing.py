// This file is a silly hack. Don't do this when you grow up, kids.
// It's packaged into a runnable .exe using $(whatever we end up using)
// and inserted into exported windows application folders.
// ALL IT DOES is look for the file lib/run.cmd (well, lib\run.cmd), make
// sure it exists, and launch it; it only exists so that we can have a
// pretty icon for our application.
// Not tested yet.

#include <windows.h>

#define RUN_FILE_NAME L"lib\\run.cmd"

// Isn't Win32 fun?
int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Check if ./lib/run.cmd exists
    WIN32_FIND_DATA fileData;
    HANDLE handle = FindFirstFile(RUN_FILE_NAME, &fileData);
    int found = handle != INVALID_HANDLE_VALUE;
    // Oh no!
    if (!found) {
        MessageBox(
                NULL, // No parent window
                L"I can't find the file \"lib\\run.cmd\", which I need to run your sketch.\r\n"
                L"Make sure you copy the *entire* application.win32 folder whenever you move your"
                L" sketch around.", // Message (c implicitly concatenates strings)
                L"Sketchy behavior", // Title
                MB_OK // Only an "OK" button
                );
        return 1;
    }
    FindClose(handle);

    // http://www.codeproject.com/Articles/1842/A-newbie-s-elementary-guide-to-spawning-processes
    ShellExecute(
            NULL, // No parent window (again)
            L"open", // The "open" verb launches applications
            RUN_FILE_NAME,
            L"", // No parameters
            L"", // Current directory
            SW_SHOW // Show the processing window!
            );

    return 0;
}
