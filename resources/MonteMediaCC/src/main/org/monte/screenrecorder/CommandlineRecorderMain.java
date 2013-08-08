/*
 * @(#)CommandlineRecorderMain.java  1.0  2011-08-05
 * 
 * Copyright (c) 2011 Werner Randelshofer, Goldau, Switzerland.
 * All rights reserved.
 * 
 * You may not use, copy or modify this file, except in compliance with the
 * license agreement you entered into with Werner Randelshofer.
 * For details see accompanying license terms.
 */
package org.monte.screenrecorder;

import java.awt.*;
import java.awt.event.*;

import java.net.URL;

import javax.swing.JButton;
import javax.swing.ImageIcon;
import javax.swing.JWindow;
import org.monte.media.Format;
import java.io.File;
import org.monte.media.math.Rational;
import static org.monte.media.AudioFormatKeys.*;
import static org.monte.media.VideoFormatKeys.*;


/**
 * {@code CommandlineRecorderMain}.
 *
 * @author Werner Randelshofer
 * @version 1.0 2011-08-05 Created.
 */
public class CommandlineRecorderMain implements ActionListener {

    ScreenRecorder sr;
    GraphicsConfiguration gc;
    JWindow window;
    JButton component;
    boolean started = false;
    String quicktimePath;
    
    URL play_url = ClassLoader.getSystemResource("org/monte/screenrecorder/images/play_button.png");
    URL rec_url = ClassLoader.getSystemResource("org/monte/screenrecorder/images/rec_button.png");
    
    public void actionPerformed(ActionEvent e) { 
        
        if (!started) {
            // start recording
            
            float quality = 0.85f; // 85% Jpeg quality
            int bitDepth = 24;
            int fps = 30;
            
            Rectangle areaRect = gc.getBounds();
            
            File quicktimeFileObj = new File(quicktimePath);
            
            String mimeType = MIME_QUICKTIME;
            String videoFormatName = ENCODING_QUICKTIME_JPEG;
            String compressorName = COMPRESSOR_NAME_QUICKTIME_JPEG;
            String crsr = ScreenRecorder.ENCODING_BLACK_CURSOR;
            
            int mov_width = 1100;
            int mov_height = (int) ((float)mov_width * ((float)areaRect.height/(float)areaRect.width));
            
            try {
                sr = new ScreenRecorder(gc, 
                                        areaRect,
                                        // the file format
                                        new Format(MediaTypeKey, MediaType.FILE, MimeTypeKey, mimeType),
                                        // the output format for screen capture:
                                        new Format(MediaTypeKey, MediaType.VIDEO, 
                                                   EncodingKey, videoFormatName,
                                                   CompressorNameKey, compressorName,
                                                   WidthKey, mov_width,
                                                   HeightKey, mov_height,
                                                   DepthKey, bitDepth, 
                                                   FrameRateKey, Rational.valueOf(fps),
                                                   QualityKey, quality,
                                                   KeyFrameIntervalKey, (int) (fps * 60) // one keyframe per minute
                                                   ),
                                        // the output format for mouse capture
                                        new Format(MediaTypeKey, MediaType.VIDEO, EncodingKey, crsr, FrameRateKey, Rational.valueOf(fps)),
                                        // the output format for audio capture
                                        null,
                                        // path to quicktime
                                        quicktimeFileObj);
                
                sr.start();
                
            } catch (Exception ex) {
                System.out.println("Exception raised while trying to start screen recording: " + ex);
                System.exit(0);
            }
            
            window.getContentPane().setBackground( Color.RED );  
            component.setLabel("Now Recording - Click here to finish!");
            Toolkit kit = Toolkit.getDefaultToolkit();
            Image img = kit.createImage(rec_url);
            component.setIcon(new ImageIcon(img));
            
            started = true;
            
        } else {
         
            // stop recording
            try {
                sr.stop();
            } catch (Exception ex) {
                // ignore
                System.out.println("Exception raised while stopping: " + ex);
            }
        
            System.exit(0);        
        }
        
    }    
    
    public void main(String quicktimePath) {

        gc = GraphicsEnvironment.getLocalGraphicsEnvironment().getDefaultScreenDevice().getDefaultConfiguration();

        this.quicktimePath = quicktimePath;

        window = new JWindow(null, gc);        
        window.setAlwaysOnTop(true);
        component = new JButton("Screen Recording - Click here to start!");
        component.addActionListener(this);
        component.setSize(500, 55);
        window.getContentPane().setBackground( Color.GREEN );  
        window.getContentPane().add(component, BorderLayout.CENTER);
        window.setSize(500, 55);
        window.setVisible(true);
        
        Toolkit kit = Toolkit.getDefaultToolkit();
        Image img = kit.createImage(play_url);
        component.setIcon(new ImageIcon(img));
        
        
    }
}
