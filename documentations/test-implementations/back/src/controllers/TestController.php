<?php

namespace Controllers;

use Jurosh\PDFMerge\PDFMerger;
use SaboCore\Routing\Response\ResourceResponse;

class TestController extends CustomController{
    public function juroshpdfmerge(){
        $pdfMerger = new PDFMerger();

        foreach($_FILES["pdf"]["tmp_name"] as $tmpName)
            $pdfMerger->addPDF($tmpName);

        return $pdfMerger->merge();
    }
}