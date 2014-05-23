package jycessing.mode.run;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ModeService extends Remote {
  void handleReady(String editorId, final SketchService service) throws RemoteException;

  void handleSketchStopped(String editorId) throws RemoteException;

  void handleSketchException(String editorId, Exception e) throws RemoteException;

  void print(String editorId, Stream stream, String s) throws RemoteException;

  void println(String editorId, Stream stream, String s) throws RemoteException;
}
