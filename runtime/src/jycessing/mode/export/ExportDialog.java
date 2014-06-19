package jycessing.mode.export;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.Rectangle;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

import processing.app.Sketch;
import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;

@SuppressWarnings("serial")
public class ExportDialog extends JDialog {
  
  @SuppressWarnings("unused")
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(ExportDialog.class.getSimpleName() + ": " + msg);
    }
  }
  
  private final Sketch sketch;
  private final PyEditor editor;
  private final JOptionPane optionPane;
  
  public ExportDialog(PyEditor editor, Sketch sketch) {
    super(editor, "Export Application", true);
    
    this.editor = editor;
    this.sketch = sketch;
    
    log("Setting up export dialog");
    
    JPanel panel = new JPanel();
    panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
    panel.add(Box.createVerticalStrut(6));
    JLabel filler = new JLabel("Options will go here", SwingConstants.CENTER);
    filler.setAlignmentX(Component.LEFT_ALIGNMENT);
    panel.add(filler);
    String[] options = { "Export", "Cancel" };
    optionPane = new JOptionPane(panel,
                                 JOptionPane.PLAIN_MESSAGE,
                                 JOptionPane.YES_NO_OPTION,
                                 null,
                                 options,
                                 options[0]);
    
    this.setContentPane(optionPane);
    optionPane.addPropertyChangeListener(new PropertyChangeListener() {
      public void propertyChange(PropertyChangeEvent e) {
        String prop = e.getPropertyName();

        if (isVisible() &&
            (e.getSource() == optionPane) &&
            (prop.equals(JOptionPane.VALUE_PROPERTY))) {
          setVisible(false);
        }
      }
    });
    this.pack();
    this.setResizable(false);
    
    Rectangle bounds = editor.getBounds();
    Dimension size = this.getSize();
    this.setLocation(bounds.x + (bounds.width - size.width) / 2,
                       bounds.y + (bounds.height - size.height) / 2);
    
  }
  
  public void go() {
    log("Launching export dialog");
    
    this.setVisible(true);
    
    // wait until they click "Export". This stops the main editor from working -
    // do we want that?
    Object value = optionPane.getValue();
    
    if (value.equals("Export")) {
      new Exporter(editor, sketch).export();
    } else {
      editor.statusNotice("Export to Application Cancelled");
    }
  }
}
