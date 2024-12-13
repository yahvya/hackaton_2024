<?php

namespace Controllers;

use PdfPseudoApp\App\PdfPseudoApp;
use PdfPseudoApp\Utils\DefaultLogger;
use PDO;
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
        if(!array_key_exists(key: "pdfs",array: $_FILES))
            ApplicationRouter::unauthorized(["error" => "Please provide a pdf file"]);

        # init logger
        $logger = new DefaultLogger(logFileAbsolutePath: APP_ROOT . "private-storage/log.txt");

        # convert to normalized arrays
        $normalizedDatas = [];

        foreach($_FILES["pdfs"]["tmp_name"] as $index => $tmpName) {
            $normalizedDatas[] = [
                "tmp_name" => $tmpName,
                "name" => $_FILES["pdfs"]["name"][$index],
                "type" => $_FILES["pdfs"]["type"][$index],
                "size" => $_FILES["pdfs"]["size"][$index],
                "error" => $_FILES["pdfs"]["error"][$index]
            ];
        }

        # check the provided file security
        if(!PdfPseudoApp::isUploadedFileSecure(fileDatas: $normalizedDatas,logger: $logger))
            ApplicationRouter::unauthorized(message: ["error" => "Please send a valid pdf file"]);

        $pdfPseudoApp = new PdfPseudoApp(
            pdfFilePaths: array_map(fn(array $datas):string => $datas["tmp_name"],$normalizedDatas),
            pythonScriptPath: APP_ROOT . "data-extraction/app.py",
            privateStoragePath: APP_ROOT . "private-storage/anonymous/",
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
     * @brief reload the entities
     * @return never
     */
    public function reload():never{
        $this->renderJson(PdfPseudoApp::reload(APP_ROOT . "private-storage/rebuild/",APP_ROOT . "data-extraction/app.py"));
    }

    /**
     * @brief set status
     * @return never
     */
    public function status():never{
        if(!array_key_exists(key: "id",array: $_POST) || !array_key_exists("status",array: $_POST))
            ApplicationRouter::unauthorized(["error" => "Please provide data"]);

        $pdo = new PDO("mysql:host=localhost;dbname=hackathon_2024", "root", "");
        $request = $pdo->prepare("UPDATE anonymisation SET status=? WHERE id=?");

        $this->renderJson(["success" => $request->execute([
            $_POST["status"],
            $_POST["id"],
        ])]);
    }
}