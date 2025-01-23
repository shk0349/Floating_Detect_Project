package edu.mbc.Detect_Boot.Detect_Boot.Controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @GetMapping("/")    //... Test OK
    public String Home() {
        return "main";    //... resources/templates/index.html을 찾아감
    }
}