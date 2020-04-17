//
//  GraphingViewController.swift
//  getAudio
//
//  Created by Varun Nair on 4/6/20.
//  Copyright © 2020 Varun Nair. All rights reserved.
//

import UIKit
import Accelerate

class GraphingViewController: UIViewController
{
    let shapeLayer = CAShapeLayer()
    let audioGet = trial2ViewController()
    
    func displayWaveInLayer(_ targetLayer: CAShapeLayer, ofColor color: UIColor, signal: [Float], min: Float?, max: Float?, hScale: CGFloat)
    {
        DispatchQueue.main.async{
            GraphUtility.drawGraphInLayer(targetLayer, strokeColor: color.cgColor, lineWidth: 3, values: signal, minimum: min, maximum: max, hScale: hScale)
        }
    }

//    override func viewDidLoad()
//    {
//        super.viewDidLoad()
//        view.layer.addSublayer(shapeLayer)
//
//        let signalToDenoise = audioGet.sampler()
//
//        displayWaveInLayer(shapeLayer, ofColor: .red, signal: signalToDenoise, min: -0.03, max: 0.05, hScale: 4)
//    }
    
    override func viewDidLayoutSubviews()
    {
    super.viewDidLayoutSubviews()
        shapeLayer.frame = view.frame.insetBy(dx: 0, dy: 50)
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
