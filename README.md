# Omok
소켓을 연결해서 즐기는 1;1 오목대전


소켓을 연결해서 즐기는 1:1 오목대전입니다

(흑돌)클라이언트 ㅡ> 서버 <ㅡ 클라이언트(백돌)
클라이언트는 서버에게 어떤 좌표에 돌을 놓았는지 위치정보를 전송합니다
서버는 클라이언트에게서 좌표값을 받아 본인이 갖고있는 위치정보 넘파이배열(오목성공 여부를 찾기 위해 2차원 넘파이배열을 사용)에 저장합니다
해당 위치정보를 기준으로 오목에 성공하였는지 판단합니다. 성공했으면 게임이 종료되고, 실패하였으면 턴을 넘기기 위해 위치정보를 전송합니다.
상대편 클라이언트에게 상대가 어떤곳을 눌렀는지 위치정보를 전송합니다
상대가 놓은 돌의 위치정보를 전송받은 클라이언트는 그 정보를 토대로 본인의 바둑판 위에 돌을 놓고 저장한 후 턴을 가져옵니다.

위가 무한으로 반복되며 오목을 달성하면 게임이 끝납니다.