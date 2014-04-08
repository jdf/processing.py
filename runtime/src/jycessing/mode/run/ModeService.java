package jycessing.mode.run;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ModeService extends Remote {
  void handleReady() throws RemoteException;

  void handleSketchStopped() throws RemoteException;

  void handleSketchException(Exception e) throws RemoteException;
}
