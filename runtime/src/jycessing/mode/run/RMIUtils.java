package jycessing.mode.run;

import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.RMIClientSocketFactory;
import java.rmi.server.RMIServerSocketFactory;
import java.rmi.server.UnicastRemoteObject;

import jycessing.mode.PythonMode;

public class RMIUtils {
  private static final boolean EXTREMELY_VERBOSE = false;

  static final int RMI_PORT = 8220;

  private static final RMIClientSocketFactory clientFactory = Socket::new;

  private static final RMIServerSocketFactory serverFactory =
    port -> new ServerSocket(port, 50, InetAddress.getLoopbackAddress());

  static {
    System.setProperty("sun.rmi.transport.tcp.localHostNameTimeOut", "1000");
    System.setProperty("java.rmi.server.hostname", "127.0.0.1");

    // Timeout RMI calls after 1.5 seconds. Good for detecting a hanging sketch runner.
    System.setProperty("sun.rmi.transport.tcp.responseTimeout", "1500");

    if (EXTREMELY_VERBOSE) {
      System.setProperty("java.rmi.server.logCalls", "true");
      System.setProperty("sun.rmi.server.logLevel", "VERBOSE");
      System.setProperty("sun.rmi.client.logCalls", "true");
      System.setProperty("sun.rmi.transport.tcp.logLevel", "VERBOSE");
    }
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

  private RMIUtils() {}

  private static Registry registry;

  public static Registry registry() throws RemoteException {
    if (registry == null) {
      try {
        registry = LocateRegistry.createRegistry(RMI_PORT, clientFactory, serverFactory);
        System.err.println("created registry at port " + RMI_PORT);
      } catch (final RemoteException e) {
        System.err.println("could not create registry; assume it's already created");
        registry = LocateRegistry.getRegistry("127.0.0.1", RMI_PORT, clientFactory);
      }
    }
    return registry;
  }

  public static void bind(final Remote remote, final Class<? extends Remote> remoteInterface)
      throws RMIProblem {
    final String registryKey = remoteInterface.getSimpleName();
    try {
      export(remote);
      log("Attempting to bind instance of " + remote.getClass().getName() + " to registry as "
          + registryKey);
      registry().bind(registryKey, remote);
      log("Bound.");
      Runtime.getRuntime().addShutdownHook(new Thread(() -> {
        try {
          log("Unbinding " + registryKey + " from registry.");
          registry().unbind(registryKey);
        } catch (final Exception ignored) {
        }
      }));
    } catch (final Exception e) {
      throw new RMIProblem(e);
    }
  }

  public static void export(final Remote remote) throws RMIProblem {
    try {
      UnicastRemoteObject.exportObject(remote, 0);
    } catch (final RemoteException e) {
      throw new RMIProblem(e);
    }
  }

  @SuppressWarnings("unchecked")
  public static <T extends Remote> T lookup(final Class<T> klass) throws RMIProblem {
    try {
      log("Looking up ModeService in registry.");
      return (T)registry().lookup(klass.getSimpleName());
    } catch (final Exception e) {
      throw new RMIProblem(e);
    }
  }
}
