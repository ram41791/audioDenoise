//
//  extensions.swift
//  getAudio
//
//  Created by Varun Nair on 4/13/20.
//  Copyright © 2020 Varun Nair. All rights reserved.
//

import UIKit

extension String
{
    func size(withSystemFontSize pointSize: CGFloat)-> CGSize
    {
        return (self as NSString).size(withAttributes: [NSAttributedString.Key.font: UIFont.systemFont(ofSize: pointSize)])
    }
}

extension CGPoint {
    func adding(x: CGFloat) -> CGPoint { return CGPoint(x: self.x + x, y: self.y) }
    func adding(y: CGFloat) -> CGPoint { return CGPoint(x: self.x, y: self.y + y) }
}
