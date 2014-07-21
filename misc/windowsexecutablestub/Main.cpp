// This file is a silly hack. Don't do this when you grow up, kids.
// It's copied along with the mode and inserted into exported windows 
// application folders.
// ALL IT DOES is look for the file lib/run.cmd (well, lib\run.cmd), make
// sure it exists, and launch it; it only exists so that we can have a
// pretty icon for our application.

#define _UNICODE

#include "strsafe.h"
#include <Windows.h>
#include <cstdlib>

// MAXIMUM POSSIBLE filename length on windows, apparently. Memory is cheap.
#define NAMEBUF_LENGTH 32767

int WINAPI WinMain(
	_In_  HINSTANCE hInstance,
	_In_  HINSTANCE hPrevInstance,
	_In_  LPSTR lpCmdLine,
	_In_  int nCmdShow
	)
{
	WCHAR *namebuf = new WCHAR[NAMEBUF_LENGTH];

	// Gets the name of the running executable file.
	GetModuleFileNameW(NULL, namebuf, NAMEBUF_LENGTH);

	// If our buffer is somehow not big enough.
	if (GetLastError() != ERROR_SUCCESS) {
		MessageBoxW(
			NULL, // No parent window
			L"I can't figure out where I am. Something is terribly wrong.\r\n"
			L"Try running the lib/run.cmd file directly.", // Message string
			L"Sketchy Behavior", // Title
			MB_OK
			);
		exit(EXIT_FAILURE);
	}

	// Concatenate executable directory and \..\lib\run.cmd; \.. is the easiest
	// way to access a parent directory without messing with strings
	HRESULT err = StringCbCatW(namebuf, NAMEBUF_LENGTH, L"\\..\\lib\\run.cmd");
	// Might fail. Somehow.
	if (FAILED(err)) {
		MessageBoxW(
			NULL,
			L"I can't figure out where I am. Something is terribly wrong.\r\n"
			L"Try running the lib/run.cmd file directly.",
			L"Sketchy Behavior",
			MB_OK
			);
		exit(EXIT_FAILURE);
	}

	// Check if lib/run.cmd exists
	WIN32_FIND_DATAW fileData;
	HANDLE handle = FindFirstFileW(namebuf, &fileData);
	int found = handle != INVALID_HANDLE_VALUE;

	// Oh no!
	if (!found) {
		MessageBoxW(
			NULL,
			L"I can't find the file \"lib\\run.cmd\", which I need to run your sketch.\r\n"
			L"Make sure you copy the *entire* application.windows64 / application.windows32\r\n"
			L"folders whenever you move your sketch around.",
			L"Sketchy Behavior",
			MB_OK
			);
		exit(EXIT_FAILURE);
	}
	FindClose(handle);

	ShellExecuteW(
		NULL, // No parent window (again)
		L"open", // The "open" verb launches applications
		namebuf, // File to launch
		L"", // No parameters
		L"", // Current directory
		SW_HIDE // Hide the .cmd window that pops up - don't worry, Processing is still shown!
		);

	exit(EXIT_SUCCESS);
}

