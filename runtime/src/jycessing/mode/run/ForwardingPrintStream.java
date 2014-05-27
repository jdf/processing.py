package jycessing.mode.run;

public class ForwardingPrintStream extends WrappedPrintStream {

  private final String id;
  private final ModeService modeService;
  private final Stream stream;

  public ForwardingPrintStream(final String id, final ModeService modeService, final Stream stream) {
    super(stream.getSystemStream());
    this.id = id;
    this.modeService = modeService;
    this.stream = stream;
  }

  @Override
  public void doPrintln(final String s) {
    try {
      modeService.println(id, stream, s);
    } catch (final Exception e) {
      super.println(s);
    }
  }

  @Override
  public void doPrint(final String s) {
    try {
      modeService.print(id, stream, s);
    } catch (final Exception e) {
      super.print(s);
    }
  }
}
