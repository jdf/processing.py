package jycessing.mode.export;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.app.Util;
import processing.core.PApplet;
import processing.core.PConstants;
import processing.data.XML;

/**
 * 
 * Perform an export to Windows, using launch4j to generate the Windows executable.
 * 
 * N.B. We use relative paths for everything. This is not laziness, this solves problems:
 *      - It allows us to specify the location of the sketch consistently
 *      - It prevents parent directories with special characters from confusing java / JOGL (which loads libs dynamically)
 *      - It is guaranteed to work, since we specify working directory with <chdir />
 * 
 * N.B. We don't use launch4j's splash screen functionality because it apparently only works with a very specific breed of 24-bit BMPs.
 * Java's works just as well.
 * 
 * Structure:
 * $appdir/                        (e.g. $sketchname/application.windows32)
 *        /$sketchname.exe         (executable shell script to run the application)
 *        /source/                 (the source code of the sketch; used to run it)
 *        /lib/                    (where java imports are stored)
 *            /jycessing/          (where stuff necessary to jycessing is stored;
 *                                  everything in here is added to the classpath.)
 *            /$libname/library/   (where resources for $libname - imported with
 *                                  add_library - are stored. Not added to classpath.)
 *        /code/                   (any other code resources the user wanted to add;
 *                                  copied verbatim.)
 *        /data/                   (all non-code resources; copied verbatim.)
 *
 */
public class WindowsExport extends PlatformExport {

  @Override
  protected void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(WindowsExport.class.getSimpleName() + ": " + msg);
    }
  }

  public WindowsExport(final Arch arch, final Sketch sketch, final PyEditor editor,
      final Set<Library> libraries) {
    this.id = PConstants.WINDOWS;
    this.arch = arch;
    this.name = PConstants.platformNames[id] + arch.bits;
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
  }

  @Override
  public void export() throws IOException {
    final boolean embedJava =
        (id == PApplet.platform) && Preferences.getBoolean("export.application.embed_java")
            && arch == Exporter.processingArch;

    final File destFolder = new File(sketch.getFolder(), "application." + name);
    final File javaFolder = new File(destFolder, "java");

    copyBasicStructure(destFolder);

    if (embedJava) {
      log("Embedding java in export.");
      javaFolder.mkdirs();
      Util.copyDir(Base.getJavaHome(), javaFolder);
    }

    final XML l4jConfig = buildLaunch4jConfig(destFolder, embedJava);
    final File configFile = Files.createTempFile("config", ".xml").toFile();
    l4jConfig.save(configFile);

    runLaunch4j(configFile);

    configFile.delete();

    log("Done.");
  }

  /**
   * Construct a Processing XML object containing the configuration for launch4j.
   * Config file docs: http://launch4j.sourceforge.net/docs.html
   */
  private XML buildLaunch4jConfig(final File destFolder, final boolean embedJava) {
    log("Building launch4j configuration.");

    final String sketchName = sketch.getName();
    final boolean setMemory = Preferences.getBoolean("run.options.memory");
    final boolean presentMode = Preferences.getBoolean("export.application.fullscreen");
    final boolean stopButton = Preferences.getBoolean("export.application.stop") && presentMode;
    final File iconFile = editor.getModeContentFile("application/windows/sketch.ico");
    final File jycessingFolder = new File(destFolder, "lib/jycessing");

    final XML config = new XML("launch4jConfig");
    config.addChild("headerType").setContent("gui"); // Not a console application
    config.addChild("outfile").setContent(
        new File(destFolder, sketchName + ".exe").getAbsolutePath());
    config.addChild("dontWrapJar").setContent("true"); // We just want a launcher
    config.addChild("errTitle").setContent("Sketchy Behavior");
    config.addChild("icon").setContent(iconFile.getAbsolutePath());
    config.addChild("chdir").setContent(".");
    config.addChild(buildJREOptions(embedJava, setMemory, arch));
    config.addChild(buildRunnerOptions(presentMode, stopButton));
    config.addChild(buildClassPathOptions(jycessingFolder));
    log("Configuration done: " + config.format(0));

    return config;
  }

  /**
   * Run launch4j on a given configuration file
   */
  private void runLaunch4j(final File configFile) throws IOException {
    log("Running launch4j.");

    final File javaHome = new File(System.getProperty("java.home"));
    final File javaExecutable;
    if (PApplet.platform == PConstants.WINDOWS) {
      javaExecutable = new File(javaHome, "bin/java.exe");
    } else {
      javaExecutable = new File(javaHome, "bin/java");
    }
    if (!javaExecutable.exists()) {
      // I should proooobably throw a FileNotFoundException here
      throw new IOException("Can't find java executable. Huh?");
    }

    final File launch4jFolder = Base.getContentFile("modes/java/application/launch4j");
    if (!launch4jFolder.exists()) {
      throw new IOException("Can't find launch4j to wrap application with.");
    }

    final File launch4jJar = new File(launch4jFolder, "launch4j.jar");
    final File xstreamJar = new File(launch4jFolder, "lib/xstream.jar");

    final ProcessBuilder pb =
        new ProcessBuilder(javaExecutable.getAbsolutePath(), "-cp", launch4jJar.getAbsolutePath()
            + System.getProperty("path.separator") + xstreamJar.getAbsolutePath(),
            "net.sf.launch4j.Main", configFile.getAbsolutePath());

    if (PythonMode.VERBOSE) {
      log("Launch4j command:");
      final List<String> command = pb.command();
      for (final String s : command) {
        log("    " + s);
      }
    }
    final Process launch4jProcess = pb.start();

    if (PythonMode.VERBOSE) {
      final Thread captureOutput = new Thread(new Runnable() {
        @Override
        public void run() {
          final BufferedReader stderr =
              new BufferedReader(new InputStreamReader(launch4jProcess.getInputStream()));
          String line;
          try {
            while ((line = stderr.readLine()) != null) {
              log(line);
            }
          } catch (final Exception e) {
          }
        }
      });
      captureOutput.start();
    }

    try {
      final int result = launch4jProcess.waitFor();
      if (result != 0) {
        throw new IOException("Launch4j seems to have failed.");
      }
    } catch (final InterruptedException e) {
      throw new IOException("Launch4j seems to have been interrupted.");
    }
  }

  private XML buildJREOptions(final boolean embedJava, final boolean setMemory, final Arch arch) {
    log("Building JRE options.");
    final XML jre = new XML("jre");
    if (embedJava) {
      // note that "Path" is relative to the output executable at runtime
      jre.addChild("path").setContent("\"%EXEDIR%\\java\""); // "java" folder is next to the
                                                             // executable?
      // TODO check
    }
    // We always add the minVersion tag, which means that the sketch will always try to look for
    // Java on the system - by default when java isn't embedded, as a fallback when it is
    jre.addChild("minVersion").setContent("1.7.0_40");

    switch (arch) {
      case AMD64:
        jre.addChild("runtimeBits").setContent("64");
        break;
      case X86:
        jre.addChild("runtimeBits").setContent("32");
    }

    if (setMemory) {
      jre.addChild("initialHeapSize").setContent(Preferences.get("run.options.memory.initial"));
      jre.addChild("maxHeapSize").setContent(Preferences.get("run.options.memory.maximum"));
    }
    // https://github.com/processing/processing/issues/2239
    jre.addChild("opt").setContent("-Djna.nosys=true");
    // Set library path; NOT including environment variable %PATH%, since it will include that
    // anyway:
    // https://github.com/processing/processing/pull/2622
    // https://github.com/processing/processing/commit/b951614
    jre.addChild("opt").setContent("-Djava.library.path=\".\\lib\"");
    // Enable assertions
    jre.addChild("opt").setContent("-ea");
    // Add splash screen
    jre.addChild("opt").setContent("-splash:\"./lib/jycessing/splash.png\"");

    if (PythonMode.VERBOSE) {
      // If we're in debug mode, assume we want our exports to be, too
      jre.addChild("opt").setContent("-Dverbose=true");
    }
    return jre;
  }

  private XML buildRunnerOptions(final boolean presentMode, final boolean stopButton) {
    log("Building Runner options.");
    // Options to pass to Runner
    final List<String> runnerOptions = new ArrayList<>();
    if (presentMode) {
      runnerOptions.add("fullScreen");
      runnerOptions.add("BGCOLOR" + "=" + Preferences.get("run.present.bgcolor"));
    }
    if (stopButton) {
      runnerOptions.add(PApplet.ARGS_STOP_COLOR + "=" + Preferences.get("run.present.stop.color"));
    } else {
      runnerOptions.add(PApplet.ARGS_HIDE_STOP);
    }
    runnerOptions.add("--noredirect");
    runnerOptions.add("--exported");

    // path to the sketch to run, relative to executable
    runnerOptions.add("\"source\\" + sketch.getCode(0).getFileName() + "\"");

    final StringBuilder runnerOptionsOutput = new StringBuilder();
    for (final String o : runnerOptions) {
      runnerOptionsOutput.append(" " + o);
    }
    final XML result = new XML("cmdLine");
    result.setContent(runnerOptionsOutput.toString());
    return result;
  }

  private XML buildClassPathOptions(final File jycessingFolder) {
    log("Building classpath options.");
    final XML classPathOptions = new XML("classPath");
    classPathOptions.addChild("mainClass").setContent("jycessing.Runner");
    for (final File f : jycessingFolder.listFiles()) {
      if (f.getName().toLowerCase().endsWith(".jar") || f.getName().toLowerCase().endsWith(".zip")) {
        // Don't need to quote classpath entries, launch4j at least handles that for us
        classPathOptions.addChild("cp").setContent("./lib/jycessing/" + f.getName());
      }
    }
    return classPathOptions;
  }
}
