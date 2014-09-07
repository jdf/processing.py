package jycessing.mode.run;

import java.awt.Point;
import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ModeService extends Remote {
  void handleReady(String editorId, final SketchService service) throws RemoteException;

  void handleSketchMoved(String editorId, final Point leftTop) throws RemoteException;

  void handleSketchStopped(String editorId) throws RemoteException;

  void handleSketchException(String editorId, Exception e) throws RemoteException;

  void printStdOut(String editorId, String s) throws RemoteException;

  void printStdErr(String editorId, String s) throws RemoteException;
}
