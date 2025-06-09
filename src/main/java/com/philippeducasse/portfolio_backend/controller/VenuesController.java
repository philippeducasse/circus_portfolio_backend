package com.philippeducasse.portfolio_backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/venues")
public class VenuesController {

    @Autowired
    private VenueRepository venueRepository;

}
