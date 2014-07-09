package jycessing.mode.export;

import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JCheckBox;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import javax.swing.border.BevelBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;

import processing.app.Base;
import processing.app.ColorChooser;
import processing.app.Preferences;
import processing.app.Sketch;
import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;

/**
 * 
 * This is the export window that pops up when the user clicks [=>].
 * It tries to look as much as possible like java mode's exporter.
 * Rather than passing the options they select directly to Exporter, it sets them in their user preferences, which Exporter and the various
 * Export classes reference later.
 *
 */
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
    
    final JPanel center = createCenterPanel();
        
    final JPanel platforms = createPlatformsPanel();
    center.add(platforms);
    
    final JPanel present = createPresentPanel();
    center.add(present);
    
    final JPanel embed = createEmbedJavaPanel(platforms.getPreferredSize().width);
    center.add(embed);
    
    // I haven't tested this on a Mac yet
    if (Base.isMacOS()) {
      final JPanel signingProblems = createMacSigningWarning(platforms.getPreferredSize().width);
      center.add(signingProblems);
    }
    
    String[] options = { "Export", "Cancel" };
    optionPane = new JOptionPane(center,
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

    // Wait until they click "Export" or "Cancel"
    Object value = optionPane.getValue();
    
    if (value.equals("Export")) {
      new Exporter(editor, sketch).export();
    } else {
      editor.statusNotice("Export to Application Cancelled");
    }
  }
  
  private JPanel createCenterPanel() {
    JPanel panel = new JPanel();
    panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
    panel.add(Box.createVerticalStrut(6));
    String line1 = "Export to Application creates double-clickable,";
    String line2 = "standalone applications for the selected plaforms.";
    JLabel label1 = new JLabel(line1, SwingConstants.CENTER);
    JLabel label2 = new JLabel(line2, SwingConstants.CENTER);
    label1.setAlignmentX(Component.LEFT_ALIGNMENT);
    label2.setAlignmentX(Component.LEFT_ALIGNMENT);
    panel.add(label1);
    panel.add(label2);
    panel.add(Box.createVerticalStrut(12));
    return panel;
  }
  
  private JPanel createPlatformsPanel() {
    final JCheckBox windowsButton = new JCheckBox("Windows");
    windowsButton.setSelected(Preferences.getBoolean("export.application.platform.windows"));
    windowsButton.addItemListener(new ItemListener() {
      public void itemStateChanged(ItemEvent e) {
        Preferences.setBoolean("export.application.platform.windows", windowsButton.isSelected());
      }
    });

    final JCheckBox macosxButton = new JCheckBox("Mac OS X");
    macosxButton.setSelected(Preferences.getBoolean("export.application.platform.macosx"));
    macosxButton.addItemListener(new ItemListener() {
      public void itemStateChanged(ItemEvent e) {
        Preferences.setBoolean("export.application.platform.macosx", macosxButton.isSelected());
      }
    });

    final JCheckBox linuxButton = new JCheckBox("Linux");
    linuxButton.setSelected(Preferences.getBoolean("export.application.platform.linux"));
    linuxButton.addItemListener(new ItemListener() {
      public void itemStateChanged(ItemEvent e) {
        Preferences.setBoolean("export.application.platform.linux", linuxButton.isSelected());
      }
    });

    JPanel platformPanel = new JPanel();
    platformPanel.add(windowsButton);
    platformPanel.add(Box.createHorizontalStrut(6));
    platformPanel.add(macosxButton);
    platformPanel.add(Box.createHorizontalStrut(6));
    platformPanel.add(linuxButton);
    platformPanel.setBorder(new TitledBorder("Platforms"));
    platformPanel.setAlignmentX(Component.LEFT_ALIGNMENT);
    return platformPanel;
  }
  
  private JPanel createPresentPanel() {
    JPanel presentPanel = new JPanel();
    presentPanel.setLayout(new BoxLayout(presentPanel, BoxLayout.Y_AXIS));
    
    final JCheckBox showStopButton = new JCheckBox("Show a Stop button");
    showStopButton.setSelected(Preferences.getBoolean("export.application.stop"));
    showStopButton.addItemListener(new ItemListener() {
      public void itemStateChanged(ItemEvent e) {
        Preferences.setBoolean("export.application.stop", showStopButton.isSelected());
      }
    });
    showStopButton.setEnabled(Preferences.getBoolean("export.application.fullscreen"));
    showStopButton.setBorder(new EmptyBorder(3, 13, 6, 13));

    final JCheckBox fullScreenButton = new JCheckBox("Full Screen (Present mode)");
    fullScreenButton.setSelected(Preferences.getBoolean("export.application.fullscreen"));
    fullScreenButton.addItemListener(new ItemListener() {
      public void itemStateChanged(ItemEvent e) {
        boolean sal = fullScreenButton.isSelected();
        Preferences.setBoolean("export.application.fullscreen", sal);
        showStopButton.setEnabled(sal);
      }
    });
    fullScreenButton.setBorder(new EmptyBorder(3, 13, 3, 13));

    Box fullScreenBox = Box.createHorizontalBox();
    fullScreenBox.add(fullScreenButton);
    fullScreenBox.add(new ColorPreference("run.present.bgcolor", editor));
    fullScreenBox.add(Box.createHorizontalStrut(10));
    fullScreenBox.add(Box.createHorizontalGlue());
    presentPanel.add(fullScreenBox);
    
    Box showStopBox = Box.createHorizontalBox();
    showStopBox.add(showStopButton);
    showStopBox.add(new ColorPreference("run.present.stop.color", editor));
    showStopBox.add(Box.createHorizontalStrut(10));
    showStopBox.add(Box.createHorizontalGlue());
    presentPanel.add(showStopBox);
    
    presentPanel.setBorder(new TitledBorder("Full Screen"));
    presentPanel.setAlignmentX(Component.LEFT_ALIGNMENT);

    return presentPanel;
  }
  
  private JPanel createEmbedJavaPanel(final int divWidth) {
    JPanel embedPanel = new JPanel();
    embedPanel.setLayout(new BoxLayout(embedPanel, BoxLayout.Y_AXIS));
    
    String platformName = null;
    if (Base.isMacOS()) {
      platformName = "Mac OS X";
    } else if (Base.isWindows()) {
      platformName = "Windows (" + Base.getNativeBits() + "-bit)";
    } else if (Base.isLinux()) {
      platformName = "Linux (" + Base.getNativeBits() + "-bit)";
    }
    
    boolean embed = Preferences.getBoolean("export.application.embed_java");
    final String embedWarning =
        "<html><div width=\"" + divWidth + "\"><font size=\"2\">" + "Embedding Java will make the "
            + platformName + " application " + "larger, but it will be far more likely to work. "
            + "Users on other platforms will need to <a href=\"\">install Java 7</a>.";
    final String nopeWarning =
        "<html><div width=\"" + divWidth + "\"><font size=\"2\">"
            + "Users on all platforms will have to install the latest "
            + "version of Java 7 from <a href=\"\">http://java.com/download</a>. " + "<br/>&nbsp;";
    // "from <a href=\"http://java.com/download\">java.com/download</a>.";
    final JLabel warningLabel = new JLabel(embed ? embedWarning : nopeWarning);
    warningLabel.addMouseListener(new MouseAdapter() {
      public void mousePressed(MouseEvent event) {
        Base.openURL("http://java.com/download");
      }
    });
    warningLabel.setBorder(new EmptyBorder(3, 13, 3, 13));

    final JCheckBox embedJavaButton = new JCheckBox("Embed Java for " + platformName);
    embedJavaButton.setSelected(embed);
    embedJavaButton.addItemListener(new ItemListener() {
      public void itemStateChanged(ItemEvent e) {
        boolean selected = embedJavaButton.isSelected();
        Preferences.setBoolean("export.application.embed_java", selected);
        if (selected) {
          warningLabel.setText(embedWarning);
        } else {
          warningLabel.setText(nopeWarning);
        }
      }
    });
    embedJavaButton.setBorder(new EmptyBorder(3, 13, 3, 13));
    
    embedPanel.add(embedJavaButton);
    embedPanel.add(warningLabel);
    embedPanel.setBorder(new TitledBorder("Embed Java"));
    
    return embedPanel;
  }
  
  private JPanel createMacSigningWarning(int divWidth) {
    JPanel signPanel = new JPanel();
    signPanel.setLayout(new BoxLayout(signPanel, BoxLayout.Y_AXIS));
    signPanel.setBorder(new TitledBorder("Code Signing"));
    
    String thePain =
        "In recent versions of OS X, Apple has introduced the \u201CGatekeeper\u201D system, "
            + "which makes it more difficult to run applications like those exported from Processing. ";

    if (new File("/usr/bin/codesign_allocate").exists()) {
      thePain +=
          "This application will be \u201Cself-signed\u201D which means that Finder may report that the "
              + "application is from an \u201Cunidentified developer\u201D. If the application will not "
              + "run, try right-clicking the app and selecting Open from the pop-up menu. Or you can visit "
              + "System Preferences \u2192 Security & Privacy and select Allow apps downloaded from: anywhere. ";
    } else {
      thePain +=
          "Gatekeeper requires applications to be \u201Csigned\u201D, or they will be reported as damaged. "
              + "To prevent this message, install Xcode (and the Command Line Tools) from the App Store, or visit "
              + "System Preferences \u2192 Security & Privacy and select Allow apps downloaded from: anywhere. ";
    }
    thePain +=
        "To avoid the messages entirely, manually code sign your app. "
            + "For more information: <a href=\"\">https://developer.apple.com/developer-id/</a>";

    JLabel area =
        new JLabel("<html><div width=\"" + divWidth + "\"><font size=\"2\">" + thePain
            + "</div></html>");

    area.setBorder(new EmptyBorder(3, 13, 3, 13));
    signPanel.add(area);
    signPanel.setAlignmentX(Component.LEFT_ALIGNMENT);
    
    area.addMouseListener(new MouseAdapter() {
      public void mousePressed(MouseEvent event) {
        Base.openURL("https://developer.apple.com/developer-id/");
      }
    });
    return signPanel;
  }
  
  static class ColorPreference extends JPanel implements ActionListener {
    ColorChooser chooser;
    String prefName;
    
    public ColorPreference(String pref, final PyEditor editor) {
      prefName = pref;
      
      setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
      setPreferredSize(new Dimension(30, 20));
      setMaximumSize(new Dimension(30, 20));
      
      addMouseListener(new MouseAdapter() {
        public void mouseReleased(MouseEvent e) {
          Color color = Preferences.getColor(prefName);
          chooser = new ColorChooser(editor, true, color, "Select", ColorPreference.this);
          chooser.show();
        }
      });
    }
    
    public void paintComponent(Graphics g) {
      g.setColor(Preferences.getColor(prefName));
      Dimension size = getSize();
      g.fillRect(0, 0, size.width, size.height);
    }

    public void actionPerformed(ActionEvent e) {
      Color color = chooser.getColor();
      Preferences.setColor(prefName, color);
      repaint();
      chooser.hide();
    }
  }
}
