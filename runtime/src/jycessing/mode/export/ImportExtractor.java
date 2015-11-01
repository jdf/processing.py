package jycessing.mode.export;

import java.io.File;
import java.io.StringReader;
import java.util.HashSet;
import java.util.Set;

import jycessing.mode.PythonMode;

import org.python.antlr.ast.Call;
import org.python.antlr.ast.Str;
import org.python.antlr.base.mod;
import org.python.core.CompilerFlags;
import org.python.core.ParserFacade;

import processing.app.Base;
import processing.app.Library;
import processing.app.Messages;
import processing.app.Platform;
import processing.app.Sketch;
import processing.app.SketchCode;

/**
 * Parses pyde source files using jython's ANTLR parser, goes through all
 * function calls with a Visitor, finds all calls to add_library, and finds
 * the libraries that are being imported. This WON'T WORK if add_library
 * is reassigned or passed not-a-string. We currently only warn the user
 * if they don't pass a string.
 * 
 * TODO More stringent warnings.
 */
public class ImportExtractor {
  @SuppressWarnings("unused")
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(ImportExtractor.class.getSimpleName() + ": " + msg);
    }
  }

  private final static File[] libLocations = new File[] {
      Platform.getContentFile("modes/java/libraries"), Base.getSketchbookLibrariesFolder()};

  private final Sketch sketch;
  private final Set<Library> libraries;

  public ImportExtractor(final Sketch sketch) {
    this.sketch = sketch;
    this.libraries = new HashSet<>();
    extract();
  }

  public Set<Library> getLibraries() {
    return libraries;
  }

  private void extract() {
    final ImportVisitor visitor = new ImportVisitor();
    for (final SketchCode code : sketch.getCode()) {
      log("Examining " + code.getFileName());
      final mod ast;
      try {
        ast =
            ParserFacade.parseExpressionOrModule(new StringReader(code.getProgram()),
                code.getFileName(), new CompilerFlags());
      } catch (final Exception e) {
        System.err.println("Couldn't parse " + code.getFileName());
        // I don't like this but I'm not sure what else to do
        // I'm keeping ImportVisitor private so that I can hide visit() from users of this class
        visitor.failure = true;
        continue;
      }
      try {
        visitor.visit(ast);
      } catch (final Exception e) {
        System.err.println("Couldn't visit " + code.getFileName());
        visitor.failure = true;
      }
    }
    if (visitor.failure) {
      Messages.showWarning("Library Problems",
          "I can't figure out all of the java libraries you're using. "
              + "Your exported sketch might not work.");
    }

    for (final String libName : visitor.importNames) {
      boolean found = false;
      for (final File parent : libLocations) {
        final File libDir = new File(parent, libName);
        if (libDir.exists()) {
          if (found) {
            // we already found it!
            // TODO figure out what to do here
            System.err.println("Found multiple versions of library " + libName);
            System.err.println("Choosing one arbitrarily.");
            continue;
          }
          found = true;
          libraries.add(new Library(libDir));
        }
      }
      if (!found) {
        System.err.println("Couldn't find library " + libName);
      }
    }
  }


  private static class ImportVisitor extends org.python.antlr.Visitor {
    public final Set<String> importNames;
    public boolean failure;

    public ImportVisitor() {
      importNames = new HashSet<>();
      failure = false;
    }

    @Override
    public Object visitCall(final Call funcall) throws Exception {
      if (funcall.getInternalFunc().getToken().getText().equals("add_library")) {
        if (funcall.getInternalArgs().get(0) instanceof Str) {
          final String text = funcall.getInternalArgs().get(0).getToken().getText();
          final String lib = text.substring(1, text.length() - 1);
          importNames.add(lib);
          log("Found library: " + lib);
        } else {
          System.err
              .println("I can't figure out what libraries you're using if you don't pass a string to add_library.\n"
                  + "Please replace "
                  + funcall.getInternalArgs().get(0).getToken().getText()
                  + " with the name of the library you're importing.");
          failure = true;
        }
      }
      return super.visitCall(funcall);
    }
  }

}
