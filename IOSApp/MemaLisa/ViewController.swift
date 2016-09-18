//
//  ViewController.swift
//  MemaLisa
//
//  Created by Sumner Hearth on 9/17/16.
//  Copyright © 2016 Sumner Hearth. All rights reserved.
//

import UIKit
import MobileCoreServices

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    @IBOutlet weak var imageView: UIImageView!
    var imagelabel: UILabel?
    var newMedia: Bool?

    @IBAction func useCamera(sender: AnyObject) {
        if UIImagePickerController.isSourceTypeAvailable(
            UIImagePickerControllerSourceType.camera) {
            
            let imagePicker = UIImagePickerController()
            
            imagePicker.delegate = self
            imagePicker.sourceType =
                UIImagePickerControllerSourceType.camera
            imagePicker.mediaTypes = [(kUTTypeImage as NSString) as String]
            imagePicker.allowsEditing = false
            
            self.present(imagePicker, animated: true,
                                       completion: nil)
            newMedia = true
            if self.imagelabel != nil {
                self.imagelabel?.isHidden = true
            }
        }
    }
    
    @IBAction func useCameraRoll(sender: AnyObject) {
        
        if UIImagePickerController.isSourceTypeAvailable(
            UIImagePickerControllerSourceType.savedPhotosAlbum) {
            let imagePicker = UIImagePickerController()
            
            imagePicker.delegate = self
            imagePicker.sourceType =
                UIImagePickerControllerSourceType.photoLibrary
            imagePicker.mediaTypes = [(kUTTypeImage as NSString) as String]
            imagePicker.allowsEditing = false
            self.present(imagePicker, animated: true,
                                       completion: nil)
            newMedia = false
            if self.imagelabel != nil {
                self.imagelabel?.isHidden = true
            }
        }
    }
    
    @IBAction func identifyImage(sender: AnyObject){
        if (imageView.image != nil){
                let url = NSURL(string: "http://192.168.0.23:1708/api/classify")
                
                let request = NSMutableURLRequest(url: url! as URL)
                request.httpMethod = "POST"
                
                let boundary = "jkhdjkflshdfjklhs"
                //define the multipart request type
                
                request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
                
                if (imageView.image == nil)
                {
                    return
                }
                
                let image_data = UIImageJPEGRepresentation(imageView.image!,0.5)
            
                
                if(image_data == nil)
                {
                    return
                }
                
                
                let body = NSMutableData()
                
                let fname = "test.jpg"
                let mimetype = "image/jpg"
                
                //define the data post parameter
                
                body.append("--\(boundary)\r\n".data(using: String.Encoding.utf8)!)
                body.append("Content-Disposition:form-data; name=\"test\"\r\n\r\n".data(using: String.Encoding.utf8)!)
                body.append("hi\r\n".data(using: String.Encoding.utf8)!)
                
                body.append("--\(boundary)\r\n".data(using: String.Encoding.utf8)!)
                body.append("Content-Disposition:form-data; name=\"file\"; filename=\"\(fname)\"\r\n".data(using: String.Encoding.utf8)!)
                body.append("Content-Type: \(mimetype)\r\n\r\n".data(using: String.Encoding.utf8)!)
                body.append(image_data!)
                body.append("\r\n".data(using: String.Encoding.utf8)!)
                
            
                body.append("--\(boundary)--\r\n".data(using: String.Encoding.utf8)!)
            
                request.httpBody = body as Data
            
                let session = URLSession.shared
                
                
                let task = session.dataTask(with: request as URLRequest) {
                    ( data, response, error) in
                    guard let _:NSData = data as NSData?, let _:URLResponse = response, error == nil else {
                        print("error")
                        return
                    }
                    
                    let dataString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
                    print(dataString)
                    
                    if (dataString) != nil{
                        let clasurl = NSURL(string: "http://192.168.0.23:1708/api/classify/"+(dataString! as String))
                        let request = NSMutableURLRequest(url:clasurl as! URL);
                        request.httpMethod = "GET"
                        
                        let task = URLSession.shared.dataTask(with: request as URLRequest) {
                            data, response, error in
                            
                            // Check for error
                            if error != nil
                            {
                                print("error=\(error)")
                                return
                            }
                            
                            // Print out response string
                            let responseString = NSString(data: data!, encoding: String.Encoding.utf8.rawValue)
                            print("responseString = \(responseString)")
                            
                            DispatchQueue.main.async(execute: {
                                if self.imagelabel == nil {
                                    // CGRectMake has been deprecated - and should be let, not var
                                    self.imagelabel = UILabel(frame: CGRect(x: 0, y: 0, width: 300, height: 36))
                                    // you will probably want to set the font (remember to use Dynamic Type!)
                                    self.imagelabel?.font = self.imagelabel?.font.withSize(36)
                                    // and set the text color too - remember good contrast
                                    self.imagelabel?.textColor = .white
                                    // may not be necessary (e.g., if the width & height match the superview)
                                    // if you do need to center, CGPointMake has been deprecated, so use this
                                    self.imagelabel?.center = CGPoint(x: 180, y: 50)
                                    // this changed in Swift 3 (much better, no?)
                                    self.imagelabel?.textAlignment = .center
                                }
                                self.imagelabel?.isHidden = false
                                self.imagelabel?.text = responseString as String?
                                self.view.addSubview(self.imagelabel!)
                            })
                        }
                        task.resume()
                    }
                    
                }
                task.resume()
        }
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        let mediaType = info[UIImagePickerControllerMediaType] as! String
        
        self.dismiss(animated: true, completion: nil)
        
        if mediaType == (kUTTypeImage as String) {
            let image = info[UIImagePickerControllerOriginalImage]
                as! UIImage
        
                imageView.image = image
        
            if (newMedia == true) {
                UIImageWriteToSavedPhotosAlbum(image, self,
                                #selector(ViewController.image(image:didFinishSavingWithError:contextInfo:)), nil)
            }
        }
    }
    
    func image(image: UIImage, didFinishSavingWithError error: NSError?, contextInfo:UnsafeRawPointer)       {
        
        if error != nil {
            let alert = UIAlertController(title: "Save Failed",
                                          message: "Failed to save image",
                                          preferredStyle: UIAlertControllerStyle.alert)
            
            let cancelAction = UIAlertAction(title: "OK",
                                             style: .cancel, handler: nil)
            
            alert.addAction(cancelAction)
            self.present(alert, animated: true,
                                       completion: nil)
        } else {
            print("Worked")
        }
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        self.dismiss(animated: true, completion: nil)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        imageView.image = UIImage(named: "mona.jpg", in: Bundle(for: ViewController.self), compatibleWith: nil)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}

