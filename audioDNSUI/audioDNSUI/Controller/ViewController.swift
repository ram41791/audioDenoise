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
    let a = "Second"
    let b = "wav"
    let UpBucketName = "audiodns"
    
    
    func uploadAudioFile(with resource: String, type: String)
    {
        let key = "\(resource).\(type)"
        let audioPath = Bundle.main.path(forResource: resource, ofType: type)!
        let localAudioURL = URL(fileURLWithPath: audioPath)
        
        let request = AWSS3TransferManagerUploadRequest()!
        
        request.bucket = UpBucketName
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
    
    func getDocumentsURL() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        let documentsDirectory = paths[0]
        return documentsDirectory
    }
    
    
    func funcFromStack()
    {
        var completionHandler: AWSS3TransferUtilityDownloadCompletionHandlerBlock?
        completionHandler = {
            [weak self] (task, URL, data, error) -> Void in
            DispatchQueue.main.async(execute: {
                print("transfer completion OK!")
                let localFileName = "xyz.m4a",
                playFileURL = self?.getDocumentsURL().appendingPathComponent(localFileName)
                FileManager.default.createFile(atPath: (playFileURL?.path)!,
                                               contents: data,
                                               attributes: nil)
                
                if FileManager.default.fileExists(atPath: (playFileURL?.path)!) {
                    print(playFileURL as Any)
                    print("playFileURL present!") // Confirm that the file is here!
                }
            })
        }
        
        
        let expression = AWSS3TransferUtilityDownloadExpression()
        
        let transferUtility = AWSS3TransferUtility.default()
        transferUtility.downloadData(
            fromBucket: UpBucketName,
            key: "NewRecording.m4a",
            expression: expression,
            completionHandler: completionHandler
        ).continueWith {
            (task) -> AnyObject? in if let error = task.error {
                print("Error: \(error.localizedDescription)")
            }
            
            if let _ = task.result {
                // Do something with downloadTask.
                print("task.result -- OK!")
                let downloadOutput = task.result
                print("downloadOutput:\(String(describing: downloadOutput))")
            }
            return nil;
        }
        
    }
    
    
    
    func s3Downloader()
    {
        let downloadRequest = AWSS3TransferManagerDownloadRequest()!
        
        downloadRequest.bucket = UpBucketName
        downloadRequest.key = "outputs/NewRecording.m4a"
        downloadRequest.downloadingFileURL = URL(string: "https://audiodns.s3.amazonaws.com/outputs/NewRecording.m4a")
        
        let transferManager = AWSS3TransferManager.default()
        
        transferManager.download(downloadRequest).continueWith(executor: AWSExecutor.mainThread()){(task) -> Any? in
            if let error = task.error
            {
                print(error)
            }
            if task.result != nil
            {
                print("download success")
            }
            return nil
        }
        
    }
        
    
    
    func downloadAudiofile()
    {
        let request = AWSS3TransferManagerDownloadRequest()!
        request.bucket = UpBucketName
        let downloadURL: String = "https://audiodns.s3.amazonaws.com/outputs/NewRecording.m4a"
        let DURL = URL(string:downloadURL)
        request.downloadingFileURL = DURL
        request.key = "NewRecording.m4a"
        
        let transferUtil = AWSS3TransferUtility.default()
        let exp = AWSS3TransferUtilityDownloadExpression()
        
        transferUtil.downloadData(fromBucket: UpBucketName, key: "NewRecording.wav", expression: exp)
        { (task, url, data, error) in
            if error != nil
            {
                print(error!)
            }
            if error == nil
            {
                print("it worked")
            }
        }
    }
    
    @IBAction func fileUpload(_ sender: Any) //Upload button
    {
        uploadAudioFile(with: a, type: b)
    }
    @IBAction func denoise(_ sender: Any) //processing button
    {
        
    }
    
    @IBAction func fileDownload(_ sender: Any) //download button
    {
        funcFromStack()
//        s3Downloader()
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

