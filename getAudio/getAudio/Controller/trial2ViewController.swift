//
//  trial2ViewController.swift
//  getAudio
//
//  Created by Varun Nair on 4/6/20.
//  Copyright © 2020 Varun Nair. All rights reserved.
//

import UIKit
import AVKit
import Accelerate

class trial2ViewController: UIViewController, AVAudioPlayerDelegate
{
    func sampler()->[Float]
    {
        let url = URL(string: "/Users/varunnair/Desktop/AudioDNS/getAudio/getAudio/Controller/NewRecording.m4a") //(Bundle.main.url(forResource: "NewRecording", withExtension: "m4a")?.path)
        //let url = URL(string: urlStr!)
        let file = try! AVAudioFile(forReading: url!)
        let format = AVAudioFormat(commonFormat: .pcmFormatFloat32, sampleRate: file.fileFormat.sampleRate, channels: 1, interleaved: false)

        let buf = AVAudioPCMBuffer(pcmFormat: format!, frameCapacity: 1024)
        try! file.read(into: buf!)

        // this makes a copy, you might not want that
        let floatArray = (Array(UnsafeBufferPointer(start: buf?.floatChannelData![0], count:Int(buf!.frameLength))))
        return(floatArray)
    }
    
    func transfromingz()
    {
        let thresholdValue:Float = 0.09
        let toBeTransformed = sampler()
        var doubleArray = [Double]()
        for i in toBeTransformed
        {
            doubleArray.append(Double(i))
        }
        
        let forwardTransfromSetup = vDSP.DCT(count: 1024, transformType: vDSP.DCTTransformType.II)
        
        let inverseTransformSetup = vDSP.DCT(count: 1024, transformType: vDSP.DCTTransformType.III)
        
        var ForwardTransformed = forwardTransfromSetup!.transform(toBeTransformed)
        vDSP.threshold(ForwardTransformed, to: thresholdValue, with:.zeroFill , result: &ForwardTransformed)
        let inverseTransformed = inverseTransformSetup!.transform(ForwardTransformed)
        
        print(inverseTransformed)
        
    }
    
    
    
    override func viewDidLoad()
    {
        let toPrint = transfromingz()
        print(toPrint)
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
