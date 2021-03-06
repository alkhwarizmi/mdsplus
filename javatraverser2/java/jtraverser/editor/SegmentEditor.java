package jtraverser.editor;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.Window;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import jtraverser.Node;
import jtraverser.editor.usage.NumericEditor;
import mds.MdsException;
import mds.data.descriptor.Descriptor;
import mds.data.descriptor.Descriptor_A;
import mds.data.descriptor_r.Signal;

@SuppressWarnings("serial")
public class SegmentEditor extends Editor{
    public static final boolean checkData(final Node node) {
        if(node != null){
            if(node.getNumSegments() > 0) return true;
        }
        return false;
    }
    private final Node node;
    private int        segment = 0;

    public SegmentEditor(final Node node, final boolean editable, final Window window){
        super(null, editable, 2);
        this.node = node;
        try{
            node.readRecordInfo();
        }catch(final MdsException e){
            MdsException.stderr("SegmentEditor.RecordInfo", e);
            e.printStackTrace();
        }
        this.setLayout(new BorderLayout());
        final JPanel columns = new JPanel(new GridLayout(1, 2));
        columns.add(this.edit[0] = new NumericEditor(this.editable, window, "Data"));
        columns.add(this.edit[1] = new NumericEditor(this.editable, window, "Dimension"));
        this.add(columns);
        final JPanel segpane = new JPanel(new BorderLayout());
        final JSlider segments = new JSlider(0, this.node.getNumSegments() - 1, this.segment);
        segpane.add(segments, BorderLayout.CENTER);
        final JTextField text = new JTextField(9);
        text.setHorizontalAlignment(SwingConstants.CENTER);
        text.setText(Integer.toString(SegmentEditor.this.segment));
        text.setEditable(false);
        segpane.add(text, BorderLayout.WEST);
        final JLabel label = new JLabel(new StringBuilder(21).append("Segments: ").append(this.node.getNumSegments() & 0xFFFFFFFFl).toString(), SwingConstants.CENTER);
        label.setBorder(BorderFactory.createEmptyBorder(0, 5, 0, 5));
        segpane.add(label, BorderLayout.EAST);
        segments.addMouseListener(new MouseAdapter(){
            @Override
            public void mouseReleased(final MouseEvent ce) {
                final int newsegment = ((JSlider)ce.getSource()).getValue();
                if(SegmentEditor.this.segment == newsegment) return;
                SegmentEditor.this.setSegment(newsegment);
            }
        });
        segments.addChangeListener(new ChangeListener(){
            @Override
            public void stateChanged(final ChangeEvent ce) {
                text.setText(Integer.toString(((JSlider)ce.getSource()).getValue()));
            }
        });
        this.add(segpane, BorderLayout.NORTH);
        this.setSegment(0);
    }

    @Override
    public final Descriptor<?> getData() throws MdsException {
        MdsException.handleStatus(MdsException.TreeINVRECTYP);
        return null;
    }

    public final Descriptor_A<?> getSegmentData() throws MdsException {
        return (Descriptor_A<?>)this.edit[0].getData();
    }

    public final Descriptor<?> getSegmentDim() throws MdsException {
        return this.edit[1].getData();
    }

    public final int getSegmentIdx() {
        return this.segment;
    }

    @Override
    public final void reset(final boolean hard) {
        this.setSegment(this.segment);
    }

    @Override
    public final void setData(final Descriptor<?> data) {/*NOP*/}

    public final void setSegment(final int segment) {
        final Signal signal;
        try{
            this.data = signal = this.node.nid.getSegment(segment);
            this.segment = segment;
            this.edit[0].setData(signal.getValue());
            this.edit[1].setData(signal.getDimension());
        }catch(final MdsException e){
            MdsException.stderr("SignalEditor", e);
            this.data = null;
            this.segment = -1;
        }
    }
}