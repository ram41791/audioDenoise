//
//  ViewController.swift
//  audioDNSUI
//
//  Created by Varun Nair on 6/17/20.
//  Copyright © 2020 Varun Nair. All rights reserved.
//

import UIKit
import AVKit
import AVFoundation
import AWSS3
import AWSCognito


class ViewController: UIViewController
{
    let bucketName = "audiodns"
    
    func uploadAudioFile(with resource: String, type: String)
    {
        let key = "\(resource).\(type)"
        let audioPath = Bundle.main.path(forResource: resource, ofType: type)!
        let localAudioURL = URL(fileURLWithPath: audioPath)
        
        let request = AWSS3TransferManagerUploadRequest()!
        
        request.bucket = bucketName
        request.key = key
        request.body = localAudioURL
        request.acl = .publicReadWrite
        
        let transferManager = AWSS3TransferManager.default()
        
        transferManager.upload(request).continueWith(executor: AWSExecutor.mainThread()) { (task) -> Any? in
            if let error = task.error
            {
                print(error)
            }
            if task.result != nil
            {
                print("upload success \(key)")
            }
            return nil
        }
    }
    
    @IBAction func fileUpload(_ sender: Any)
    {
        uploadAudioFile(with: "Second", type: "wav")
    }
    @IBAction func denoise(_ sender: Any)
    {
        
    }
    
    @IBAction func fileDownload(_ sender: Any)
    {
        
    }
    
    
    override func viewDidLoad()
    {
        super.viewDidLoad()
        
        let credentialsProvider = AWSCognitoCredentialsProvider(regionType:.USEast1,
           identityPoolId:"us-east-1:595c9505-1591-4089-9127-271ee18555ec")

        let configuration = AWSServiceConfiguration(region:.USEast1, credentialsProvider:credentialsProvider)

        AWSServiceManager.default().defaultServiceConfiguration = configuration


        // Do any additional setup after loading the view.
    }


}

