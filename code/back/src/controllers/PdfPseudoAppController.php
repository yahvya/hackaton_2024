<?php

namespace Controllers;

use PdfPseudoApp\App\PdfPseudoApp;
use PdfPseudoApp\Utils\DefaultLogger;
use Routing\ApplicationRouter;
use Throwable;

/**
 * @brief pdf app treatment controller
 */
class PdfPseudoAppController extends AbstractController {
    /**
     * @brief provide the entities to mask for the provided pdf
     * @return never
     */
    public function provideEntities():never{
        if(!array_key_exists(key: "pdf",array: $_FILES))
            ApplicationRouter::unauthorized(["error" => "Please provide a pdf file"]);

        # init logger
        $logger = new DefaultLogger(logFileAbsolutePath: APP_ROOT . "private-storage/log.txt");

        # check the provided file security
        if(!PdfPseudoApp::isUploadedFileSecure(fileData: $_FILES["pdf"],logger: $logger))
            ApplicationRouter::unauthorized(message: ["error" => "Please send a valid pdf file"]);

        $pdfPseudoApp = new PdfPseudoApp(
            pdfFilePath: $_FILES["pdf"]["tmp_name"],
            pythonScriptPath: APP_ROOT . "data-extraction/script.py",
            privateStoragePath: APP_ROOT . "private-storage/",
            logger: $logger
        );

        try{
            $this->renderJson(json: $pdfPseudoApp->getEntitiesToTransform());
        }
        catch(Throwable){
            ApplicationRouter::internalError();
        }
    }

    /**
     * @brief save the final pdf to treat
     * @return never
     */
    public function save():never{

        $this->renderJson(json: []);
    }
}