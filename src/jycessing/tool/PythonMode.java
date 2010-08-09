/*
 * Copyright 2010 Jonathan Feinberg
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package jycessing.tool;

import processing.app.Editor;
import processing.app.tools.Tool;

public class PythonMode implements Tool {
	private Editor editor;

	public String getMenuTitle() {
		return "Python Mode";
	}

	public void init(final Editor editor) {
		this.editor = editor;
	}

	public void run() {
		editor.deactivateExport();
		editor.setHandlers(new RunHandler(), new PresentHandler(), new StopHandler(),
				new ExportHandler(), new ExportAppHandler());
		editor.statusNotice("Python Mode initialized.");
	}

	private class ExportHandler implements Runnable {
		public void run() {
			editor.statusError("Export not implemented in Python mode.");
		}
	}

	private class StopHandler implements Runnable {
		public void run() {
			editor.statusError("Stop not implemented in Python mode.");
		}
	}

	class PresentHandler implements Runnable {
		public void run() {
			editor.statusError("Present not implemented in Python mode.");
		}
	}

	class RunHandler implements Runnable {
		public void run() {
			editor.statusError("Run not implemented in Python mode.");
		}
	}

	class ExportAppHandler implements Runnable {
		public void run() {
			editor.statusError("Export Application not implemented in Python mode.");
		}
	}
}
