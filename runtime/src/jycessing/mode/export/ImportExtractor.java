package jycessing.mode.export;

import java.io.File;
import java.io.FileReader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import jycessing.mode.PythonMode;

import org.python.antlr.PythonTree;
import org.python.antlr.Visitor;
import org.python.antlr.ast.Call;
import org.python.antlr.ast.Str;
import org.python.antlr.base.mod;
import org.python.core.CompilerFlags;
import org.python.core.ParserFacade;

import processing.app.Library;
import processing.app.Sketch;
import processing.app.SketchCode;
import processing.app.Base;

public class ImportExtractor {
  @SuppressWarnings("unused")
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(ImportExtractor.class.getSimpleName() + ": " + msg);
    }
  }
  
  private final static File[] libLocations = new File[] {
    Base.getContentFile("modes/java/libraries"),
    Base.getSketchbookLibrariesFolder()
  };
  
  private final Sketch sketch;
  private final Set<Library> libraries;
  
  public ImportExtractor(Sketch sketch) {
    this.sketch = sketch;
    this.libraries = new HashSet<>();
    extract();
  }
  
  public Set<Library> getLibraries() {
    return libraries;
  }
  
  private void extract() {
    ImportVisitor visitor = new ImportVisitor();
    for (SketchCode code : sketch.getCode()) {
      log("Examining "+code.getFileName());
      final mod ast;
      try {
        ast = ParserFacade.parseExpressionOrModule(new StringReader(code.getProgram()), code.getFileName(), new CompilerFlags());
      } catch (Exception e) {
        System.err.println("Couldn't parse "+code.getFileName());
        // I don't like this but I'm not sure what else to do
        // I'm keeping ImportVisitor private so that I can hide visit() from users of this class
        visitor.failure = true;
        continue;
      }
      try {
        visitor.visit(ast);
      } catch (Exception e) {
        System.err.println("Couldn't visit "+code.getFileName()); 
        visitor.failure = true;
      }
    }
    if (visitor.failure) {
      // TODO stop exporting here?
      Base.showWarning("Library Problems", "I can't figure out all of the java libraries you're using. Your exported sketch might not work.");
    }
    
    for (String libName : visitor.importNames) {
      boolean found = false;
      for (File parent : libLocations) {
        final File libDir = new File(parent, libName);
        if (libDir.exists()) {
          if (found) {
            // we already found it!
            // TODO figure out what to do here
            System.err.println("Found multiple versions of library "+libName);
            System.err.println("Choosing one arbitrarily.");
            continue;
          }
          found = true;
          libraries.add(new Library(libDir));
        }
      }
      if (!found) {
        System.err.println("Couldn't find library "+libName);
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
    
    public Object visitCall(Call funcall) throws Exception {
      log("Visiting funcall: " + funcall.toStringTree());
      log(funcall.getInternalFunc().getToken().getText());
      if (funcall.getInternalFunc().getToken().getText().equals("add_library")) {
        log("Found add_library!");
        if (funcall.getInternalArgs().get(0) instanceof Str) {
          log("Argument is a string!");
          final String text = funcall.getInternalArgs().get(0).getToken().getText();
          log("String text: "+text);
          final String lib = text.substring(1, text.length()-1);
          log("Library: "+lib);
          importNames.add(lib);
        } else {
          System.out.println("Uh-oh, not string!");
          // TODO yell at the user for not using a string literal
          failure = true;
        }
      }
      return super.visitCall(funcall);
    }
  }

}
