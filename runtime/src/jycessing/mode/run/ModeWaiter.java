package jycessing.mode.run;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ModeWaiter extends Remote {
  void modeReady(ModeService modeService) throws RemoteException;
}
