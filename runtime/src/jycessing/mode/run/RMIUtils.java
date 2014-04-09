package jycessing.mode.run;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

import jycessing.mode.PythonMode;

public class RMIUtils {
  static final int RMI_PORT = 8220;

  static {
    // Timeout RMI calls after 1.5 seconds. Good for detecting a hanging sketch runner.
    System.setProperty("sun.rmi.transport.tcp.responseTimeout", "1500");
  }

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(RMIUtils.class.getSimpleName() + ": " + msg);
    }
  }

  public static class RMIProblem extends Exception {
    RMIProblem(final Exception e) {
      super(e);
    }
  }

  private RMIUtils() {
  }

  public static Registry registry() throws RemoteException {
    try {
      return LocateRegistry.createRegistry(RMI_PORT);
    } catch (RemoteException e) {
    }
    return LocateRegistry.getRegistry(RMI_PORT);
  }

  public static void
      bind(final Remote remote, final Class<? extends Remote> remoteInterface) throws RMIProblem {
    final String registryKey = remoteInterface.getSimpleName();
    log("Binding instance of " + remote.getClass().getName() + " to registry as " + registryKey);
    try {
      final Remote stub = export(remote);
      registry().bind(registryKey, stub);
      Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            log("Unbinding " + registryKey + " from registry.");
            registry().unbind(registryKey);
          } catch (Exception e) {
          }
        }
      }));
    } catch (Exception e) {
      throw new RMIProblem(e);
    }
  }

  public static Remote export(final Remote remote) throws RMIProblem {
    try {
      return UnicastRemoteObject.exportObject(remote, 0);
    } catch (RemoteException e) {
      throw new RMIProblem(e);
    }
  }

  @SuppressWarnings("unchecked")
  public static <T extends Remote> T lookup(final Class<T> klass) throws RMIProblem {
    try {
      log("Looking up ModeService in registry.");
      return (T)registry().lookup(klass.getSimpleName());
    } catch (Exception e) {
      throw new RMIProblem(e);
    }
  }
}
