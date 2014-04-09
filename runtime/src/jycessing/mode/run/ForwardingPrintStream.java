package jycessing.mode.run;

public class ForwardingPrintStream extends WrappedPrintStream {

  private final ModeService modeService;
  private final Stream stream;

  public ForwardingPrintStream(final ModeService modeService, final Stream stream) {
    super(stream.getSystemStream());
    this.modeService = modeService;
    this.stream = stream;
  }

  @Override
  public void doPrintln(String s) {
    try {
      modeService.println(stream, s);
    } catch (Exception e) {
      super.println(s);
    }
  }

  @Override
  public void doPrint(String s) {
    try {
      modeService.print(stream, s);
    } catch (Exception e) {
      super.print(s);
    }
  }
}
