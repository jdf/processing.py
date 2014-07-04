package jycessing.launcher;

import java.io.File;
import java.util.List;

import jycessing.RunnableSketch;
import jycessing.Runner.LibraryPolicy;

public class StandaloneSketch implements RunnableSketch {

  public StandaloneSketch(final String[] args) {
    
  }
  
  @Override
  public File getMainFile() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public File getHomeDirectory() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public String[] getPAppletArguments() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public List<File> getLibraryDirectories() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public LibraryPolicy getLibraryPolicy() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public String getMainCode() {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public boolean shouldRun() {
    // TODO Auto-generated method stub
    return false;
  }

}
