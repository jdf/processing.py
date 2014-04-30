package jycessing.mode.run;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface SketchService extends Remote {
  void startSketch(SketchInfo info) throws RemoteException;

  void stopSketch() throws RemoteException;

  void shutdown() throws RemoteException;
}
