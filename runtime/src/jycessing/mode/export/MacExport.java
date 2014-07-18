package jycessing.mode.export;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.util.Set;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.core.PApplet;
import processing.core.PConstants;


/**
 * 
 * A Mac export.
 * TODO implement.
 * 
 * If we embed java, we embed Processing's java, since we know it's been properly appbundled
 * and all symlinks work and stuff.
 * 
 * Layout:
 * $appdir/
 *        /$sketch.app/Contents/
 *              /MacOS/
 *                    /$sketch (shell script that cd's to ../Processing and runs the sketch)
 *              /Info.plist (holds os x stuff)
 *              /Resources/
 *                    /sketch.icns (pretty icon)
 *              /Processing/
 *                    /source/
 *                    /lib/
 *                    /code/
 *                    /data/
 *              /PlugIns/jdk$version.jdk/ (copied from core processing)
 *                     
 *
 */
public class MacExport extends PlatformExport {
  
  @Override
  protected void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(MacExport.class.getSimpleName() + ": " + msg);
    }
  }
  
  public MacExport(Sketch sketch, PyEditor editor, Set<Library> libraries) {
    this.id = PConstants.MACOSX;
    this.name = PConstants.platformNames[id];
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
    this.arch = Arch.AMD64;
  }
  
  /**
   * Copy Processing's builtin JDK to the export.
   * 
   * (This only makes sense when we're on a Mac, running Processing from a .app bundle.)
   */
  private void copyJDKPlugin(final File targetPluginsFolder) throws IOException {
    // This is how Java Mode finds it... basically
    final File sourceJDKFolder = Base.getContentFile("../PlugIns").listFiles(
        new FilenameFilter() {
          public boolean accept(File dir, String name){
            return name.endsWith(".jdk") && !name.startsWith(".");
          }
        })[0].getAbsoluteFile();
    
    log("Copying JDK from "+sourceJDKFolder);
    
    targetPluginsFolder.mkdirs();
    final File targetJDKFolder = new File(targetPluginsFolder, sourceJDKFolder.getName());
    Base.copyDirNative(sourceJDKFolder, targetJDKFolder);
  }
  
  /**
   * Copy the resources folder skeleton from $mode/application/macosx/Resources.
   */
  private void copyResourcesFolder(final File targetResourcesFolder) throws IOException {
    final File sourceResourcesFolder = new File(editor.getModeFolder(), "application/macosx/Resources").getAbsoluteFile();
    log("Copying resources from"+sourceResourcesFolder);
    Base.copyDir(sourceResourcesFolder, targetResourcesFolder);
  }
  
  /**
   * Read in Info.plist.tmpl, modify fields, package away in .app
   */
  private void setUpInfoPlist(final File targetInfoPlist) throws IOException {
    
  }
  
  @Override
  public void export() throws IOException {
    // Work out user preferences and other possibilities we care about
    final boolean embedJava =
        (id == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");
    final boolean setMemory = Preferences.getBoolean("run.options.memory");
    final boolean presentMode = Preferences.getBoolean("export.application.fullscreen");
    final boolean stopButton = Preferences.getBoolean("export.application.stop") && presentMode;
    
    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application." + name);
    final File appRootFolder = new File(destFolder, sketch.getName()+".app");
    final File contentsFolder = new File(appRootFolder, "Contents");
    final File binFolder = new File(contentsFolder, "MacOS");
    final File resourcesFolder = new File(contentsFolder, "Resources");
    final File processingFolder = new File(contentsFolder, "Processing");
    
    final File infoPlist = new File(contentsFolder, "Info.plist");
    final File script = new File(binFolder, sketch.getName());
    
    copyBasicStructure(processingFolder);
    copyResourcesFolder(resourcesFolder);
    
    if (embedJava) {
      copyJDKPlugin(new File(contentsFolder, "PlugIns"));
    }
    
    
    log("I would do a mac export here... if I knew how :(");

  }

}
