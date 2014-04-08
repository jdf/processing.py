package jycessing.mode.run;

import java.io.File;
import java.rmi.Remote;
import java.rmi.RemoteException;

import jycessing.mode.RunMode;

public interface SketchService extends Remote {
  void startSketch(RunMode runMode, File libraries, File sketch, String code, String[] codeFiles,
      int x, int y) throws RemoteException;

  void stopSketch() throws RemoteException;
}
